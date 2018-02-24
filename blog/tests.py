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
    expected = "<p></p>hackUser();<strong></strong>"
    assert utils.sanitize_html(html_one) == expected

    html_two = ('<h1>Title</h1><p>Hello</p>'
                '<code>print("Hello World!")</code>')
    assert utils.sanitize_html(html_two) == html_two

def test_json_error():
    expected = '{"error": {"code": "404", "message": "Not found"}}'
    assert utils.json_error("Not found", "404") == expected