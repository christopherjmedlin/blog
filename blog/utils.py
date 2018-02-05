from flask import session, request, redirect

from mistune import Markdown
from html_sanitizer import Sanitizer
from bs4 import BeautifulSoup

from functools import wraps
import datetime
import json

VALID_TAGS = ['strong', 'em', 'p', 'ul', 'li', 'br', 'img', 'a']

#########################
# Utility functions
#########################

def json_error(message, code=505):
    return """
    {
        "error": {
            "code": {},
            "message": {},
        }
    }
    """.format(code, message)

def sanitize_html(html):

    soup = BeautifulSoup(html, 'html.parser')

    for tag in soup.findAll(True):
        if tag.name not in VALID_TAGS:
            tag.hidden = True

    return str(soup.renderContents().decode('ascii'))

def html_preview(html):
    soup = BeautifulSoup(html, 'html.parser')

    for tag in soup.findAll(True):
        tag.hidden = True
    
    return str(soup.renderContents().decode('ascii'))

def get_first_img(html):

    soup = BeautifulSoup(html, 'html.parser')

    try:
        return soup.find_all('img')[0].get('src')
    except IndexError:
        pass
    return None

def build_next_page_url(page, topic=None, query_string=None):
    nextPage = '/posts?'
    if topic:
        nextPage += 'topic=' + topic
    if query_string:
        nextPage += '&q=' + query_string
    nextPage += '&page=' + str(page + 1)
    return nextPage

def parse_json_post_data(json_data):
    data = json.loads(json_data)
    data["posted"] = datetime.datetime.utcnow()

    markdown = Markdown()
    html = markdown(data['content'])
    html = sanitize_html(html)
    data['preview'] = html_preview(html)
    data['markdown'] = data['content']
    data['content'] = html
    data['author'] = session['username']
    data['img'] = get_first_img(html)
    return data

#########################
# Decoraters
#########################

def auth_route(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            if session['authenticated']:
                return f(*args, **kwargs)                        
            else:
                path = request.path
                return redirect('/login?redirect=' + path)
        except KeyError:
            return redirect('/login?redirect=' + request.path)

    return decorated_function