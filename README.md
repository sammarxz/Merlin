# Merlin
Merlin is simple static site generator built in python. I'm still developing it, but it can already be used to produce simple websites.

## Features(until now):

* Support [Sass](http://sass-lang.com/)
* Markdown Support
* Template engine with [Jinja2](http://jinja.pocoo.org/)
* Livereload (may contain bugs)
* Syntax Highlight with [Pygments](http://pygments.org/)

## How to use (provisionally):

```
$ git clone https://github.com/sammarxz/Merlin.git your_project_name
$ cd your_project_name
$ pip install -r requirements.txt
$ rm -rf .git
$ python manage.py
```

After running the script, go to http://localhost:8000.

Note that we've removed .git so you can create your own repository and deopis to deploy and use Gitub pages.

```
# git init
```
