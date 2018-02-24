from blog import app, mongo
from . import utils

from functools import wraps

def app_test(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        app_client = app.test_client()

    return decorated_function

#########################
# Unit Tests
#########################

def test_sanitize_html():
    html_one = "<p></p><script>hackUser();</script><strong></strong>"
    html_two = ('<h1>Title</h1><p>Hello</p>'
                '<code>print("Hello World!")</code>')
    expected_one = "<p></p>hackUser();<strong></strong>"

    assert utils.sanitize_html(html_one) == expected_one
    assert utils.sanitize_html(html_two) == html_two

def test_json_error():
    expected = '{"error": {"code": "404", "message": "Not found"}}'
    assert utils.json_error("Not found", "404") == expected

def test_html_preview():
    html_one = '<h1>Title</h1> <p>Content</p>'
    html_two = '<p>Text</p><img src="a link" />'
    assert utils.html_preview(html_one) == "Title Content"
    assert utils.html_preview(html_two) == "Text"

def test_get_first_img():
    html_one = '<h1>Title</h1> <img src="https://image.com/img.jpg" />'
    html_two = '<p>This HTML has no image</p>'
    assert utils.get_first_img(html_one) == "https://image.com/img.jpg"
    assert utils.get_first_img(html_two) == None