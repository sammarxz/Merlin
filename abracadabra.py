import datetime
import os

from jinja2 import Environment, FileSystemLoader

from livereload import Server

import mistune

import sass

import yaml


BASE_DIR = os.getcwd()
CONTENT_DIR = os.path.join(BASE_DIR, '_posts')
POSTS_DIR = os.path.join(BASE_DIR, 'posts')
TEMPLATES_DIR = os.path.join(BASE_DIR, '_templates')
DATE_FORMAT = '%Y-%m-%d'

env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

INDEX_TEMPLATE = env.get_template('layouts/index.html')
POST_TEMPLATE = env.get_template('layouts/post.html')
POSTS_TEMPLATE = env.get_template('layouts/posts.html')

SITE_TITLE = 'Merlin'
SITE_LANG = 'en'


def _convert_filename(filename):
    return filename.split('.')[0]


def generate_context(attributes):
    context = {
        'title': SITE_TITLE,
        'lang': SITE_LANG,
    }
    try:
        context.update({
            'author': attributes.get('author'),
            'category': attributes.get('category'),
            'post_title': attributes['title'],
            'post_description': attributes.get('description'),
            'date': datetime.date.strftime(attributes['date'], DATE_FORMAT),
        })
    except KeyError:
        pass
    return context


def get_all_posts():
    for entry in os.scandir(CONTENT_DIR):
        if all([
            not entry.name.startswith('.'),
            entry.name.endswith('.md'),
            entry.is_file()
        ]):
            yield entry.name


def generate_html(filename, context, template=POST_TEMPLATE,
                  output_path=POSTS_DIR):
    new_file_name = os.path.splitext(filename)[0] + '.html'
    open(os.path.join(output_path, new_file_name), 'w').write(
        template.render(context)
    )


def parse_post(file, with_content=True):
    with open(os.path.join(CONTENT_DIR, file)) as f:
        whole_file = f.read()
    yaml_header, content = whole_file.split('---', maxsplit=1)
    attributes = yaml.load(yaml_header)
    if not with_content:
        return attributes
    return attributes, content


def generate_page(page, template=INDEX_TEMPLATE, posts=None):
    context = generate_context({})
    if not posts:
        generate_html(page, context, template, output_path=BASE_DIR)
    else:
        posts = [
            {
                'title': parse_post(post, with_content=False).get('title'),
                'url': '/posts/' + _convert_filename(post) + ".html",
            } for post in posts
        ]
        context.update({'posts': posts})
        generate_html(page, context, template, output_path=BASE_DIR)


def main():
    if not os.path.exists(POSTS_DIR):
        os.mkdir(POSTS_DIR)
    posts = list(get_all_posts())
    generate_page('posts.html', template=POSTS_TEMPLATE, posts=posts)
    generate_page('index.html')
    for post in posts:
        attributes, content = parse_post(post)
        content = mistune.markdown(content, escape=True, hard_wrap=True)
        context = generate_context(attributes)
        context.update({'content': content})
        generate_html(post, context)
    sass.compile(dirname=('_sass', 'static/css'))


if __name__ == '__main__':
    main()
    server = Server()
    server.watch('**/*', main)
    server.serve(port=8000, host='localhost')
