import os

from jinja2 import Template, Environment, FileSystemLoader
import mistune

BASE_DIR = os.getcwd()
CONTENT_DIR = os.path.join(BASE_DIR, '_posts')
OUTPUT_DIR = os.path.join(BASE_DIR, 'posts')
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

env = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR)
)

with open(os.path.join(TEMPLATES_DIR, 'post.html')) as f:
    POST_TEMPLATE = Template(f.read())

def get_all_posts():
    for entry in os.scandir(CONTENT_DIR):
        if all([
            not entry.name.startswith('.'),
            entry.name.endswith('.md'),
            entry.is_file()
        ]):
            yield entry.name

def generate_html(files):
    for file in files:
        with open(os.path.join(CONTENT_DIR, file)) as f:
            content = mistune.markdown(f.read(), escape=True, hard_wrap=True)
        new_file_name = os.path.splitext(file)[0] + ".html"
        template = env.get_template('post.html')
        print(template)
        open(os.path.join(OUTPUT_DIR, new_file_name), "w").write(
            template.render(content=content)
        )

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

    generate_html(get_all_posts())

if __name__ == "__main__":
    main()