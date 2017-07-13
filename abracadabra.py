import datetime
import os

from jinja2 import Environment, FileSystemLoader
import mistune
import yaml


BASE_DIR = os.getcwd()
CONTENT_DIR = os.path.join(BASE_DIR, '_posts')
OUTPUT_DIR = os.path.join(BASE_DIR, 'posts')
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
DATE_FORMAT = '%Y-%m-%d'

env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
POST_TEMPLATE = env.get_template('layouts/post.html')
INDEX_TEMPLATE = env.get_template('layouts/index.html')

SITE_TITLE = 'Merlin'
SITE_LANG = 'en'


def generate_context(attributes):
    return {
        'title': SITE_TITLE,
        'lang': SITE_LANG,

        'post_title': attributes['title'],
        'date': datetime.date.strftime(attributes['date'], DATE_FORMAT),
        'author': attributes.get('author'),
        'category': attributes.get('category'),
        }

def get_all_posts():
    for entry in os.scandir(CONTENT_DIR):
        if all([
            not entry.name.startswith('.'),
            entry.name.endswith('.md'),
            entry.is_file()
        ]):
            yield entry.name

def generate_html(filename, context, post):
    new_file_name = os.path.splitext(filename)[0] + '.html'
    context.update({'content':post})
    open(os.path.join(OUTPUT_DIR, new_file_name), 'w').write(
        POST_TEMPLATE.render(context)
    )

def parse_post(file):
    with open(os.path.join(CONTENT_DIR, file)) as f:
        whole_file = f.read()
    yaml_header, content = whole_file.split('---', maxsplit=1)
    attributes = yaml.load(yaml_header)
    return attributes, content

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

    posts = get_all_posts()
    for post in posts:
        attributes, content = parse_post(post)
        content = mistune.markdown(content)
        context = generate_context(attributes)
        generate_html(post, context, content)

if __name__ == '__main__':
    main()