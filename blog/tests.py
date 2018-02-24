from blog import app, mongo
from . import utils, html

from functools import wraps
import json, random, string

client = app.test_client()
with client.session_transaction() as sess:
    sess["username"] = "test"

#########################
# Unit Tests
#########################

def test_sanitize_html():
    html_one = "<p></p><script>hackUser();</script><strong></strong>"
    html_two = ('<h1>Title</h1><p>Hello</p>'
                '<code>print("Hello World!")</code>')
    expected_one = "<p></p>hackUser();<strong></strong>"

    assert html.sanitize_html(html_one) == expected_one
    assert html.sanitize_html(html_two) == html_two

def test_json_error():
    expected = '{"error": {"code": "404", "message": "Not found"}}'
    assert utils.json_error("Not found", "404") == expected

def test_html_preview():
    html_one = '<h1>Title</h1> <p>Content</p>'
    html_two = '<p>Text</p><img src="a link" />'
    assert html.html_preview(html_one) == "Title Content"
    assert html.html_preview(html_two) == "Text"

def test_get_first_img():
    html_one = '<h1>Title</h1> <img src="https://image.com/img.jpg" />'
    html_two = '<p>This HTML has no image</p>'
    assert html.get_first_img(html_one) == "https://image.com/img.jpg"
    assert html.get_first_img(html_two) == None

def test_build_next_page_url():
    assert utils.build_next_page_url(1) == "/posts?&page=2"
    assert utils.build_next_page_url(3, "python", "search") == \
        "/posts?topic=python&q=search&page=4"
    assert utils.build_next_page_url(100, "topic") == \
        "/posts?topic=topic&page=101"

def test_parse_json_post_data():
    json_data = json.dumps({
        "title": "Title",
        "content": "![Image of Yaktocat](https://octodex.github.com/images/yaktocat.png)",
        "topics": ["TeST", "STuFf"]
    })
    data = utils.parse_json_post_data(json_data, "Human Being")
    assert data["img"] == "https://octodex.github.com/images/yaktocat.png"
    assert data["topics"][0] == "test"
    assert data["author"] == "Human Being"

#########################
# Integration Tests
#########################

def test_posts_create():
    content = ''.join(random.choice(string.ascii_lowercase) for i in range(20))
    response = client.post('/api/v1/posts', data=json.dumps({
        "title": "Title",
        "content": content,
        "topics": ["test", "stuff"]
    }))

    assert response.status == '200 OK'
    assert mongo.db.posts.find({"content": "<p>" + content + "</p>\n"}).count() > 0

def test_posts_delete():
    result = mongo.db.posts.insert_one({
        "title": "Title",
        "content": "Content",
        "topics": ["test", "stuff"]
    })
    id = result.inserted_id
    response = client.delete('/api/v1/posts/' + str(id))

    assert response.status == '200 OK'
    assert mongo.db.posts.find({"id": id}).count() == 0

def test_posts_update():
    result = mongo.db.posts.insert_one({
        "title": "Title",
        "content": "Content",
        "topics": ["test", "stuff"]
    })
    data = json.dumps({
        "title": "New Title",
        "content": "New Content"
    })
    id = result.inserted_id
    response = client.put('/api/v1/posts/' + str(id), data=data)

    assert response.status == '200 OK'
    assert mongo.db.posts.find_one({"_id": id})["title"] == "New Title"
    assert ("New Content" in mongo.db.posts.find_one({"_id": id})["content"])

