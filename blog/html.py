from mistune import Markdown
from html_sanitizer import Sanitizer
from bs4 import BeautifulSoup

VALID_TAGS = ['strong', 'em', 'p', 'ul', 'li', 'br', 'img', 'a', 'h1',
              'h2', 'h3', 'h4', 'h5', 'h6', 'pre', 'code']

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