from flask import session, request, redirect

from mistune import Markdown
from html_sanitizer import Sanitizer
from bs4 import BeautifulSoup

from functools import wraps
import datetime
import json

#########################
# Utility functions
#########################

def json_error(message, code=505):
    return json.dumps({
        "error": {
            "code": code,
            "message": message,
        }
    })

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
    html = html.sanitize_html(html)
    data['preview'] = html.html_preview(html)
    data['markdown'] = data['content']
    data['content'] = html
    data['author'] = session['username']
    data['img'] = html.get_first_img(html)
    
    if 'topics' in data:
        for count in range(0, len(data['topics'])):
            data['topics'][count] = data['topics'][count].lower()
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