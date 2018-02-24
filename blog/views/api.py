"""
Routes for the API
"""

from flask import render_template, Response, request, session

from bson import ObjectId
from bson.json_util import dumps

from mistune import Markdown
from html_sanitizer import Sanitizer
from bs4 import BeautifulSoup

import datetime
import json

from blog import app, mongo, utils

@app.route('/api/v1/posts', methods=['GET'])
def posts_list():
    posts = mongo.db.posts.find({})
    markdown = request.args.get("markdown", 'false')
    if markdown == 'false':
        markdown = False
    else:
        markdown = True
    return render_template('xml/posts.xml', posts=posts, markdown=markdown)

@app.route('/api/v1/posts', methods=['POST'])
def posts_create():
    data = utils.parse_json_post_data(request.data, session['username'])

    if mongo.db.posts.insert_one(data):
        return Response(status=200)
    else:
        return Response(utils.json_error("Internal database error.", 500), status=500)

@app.route('/api/v1/posts/<id>', methods=['DELETE'])
def posts_delete(id):
    mongo.db.posts.delete_one({"_id": ObjectId(id)})
    return Response(status=200)

@app.route('/api/v1/posts/<id>', methods=['GET'])
def posts_retrieve(id):
    markdown = request.args.get("markdown", 'false')
    if markdown == 'false':
        markdown = False
    else:
        markdown = True

    post = mongo.db.posts.find_one({"_id": ObjectId(id)})
    return render_template('xml/post.xml', post=post, markdown=markdown)

@app.route('/api/v1/posts/<id>', methods=['PUT'])
def posts_update(id):
    data = utils.parse_json_post_data(request.data, session['username'])
    
    if mongo.db.posts.update_one({'_id': ObjectId(id)}, {"$set": data}):
        return Response(status=200)
    else:
        return Response(utils.json_error("Internal database error.", 500), status=500)