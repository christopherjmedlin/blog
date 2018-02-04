"""
Routes that aren't for the API and usually involve rendering a template
"""

from flask import (render_template, request, session, 
                   redirect, make_response)

import pymongo
from bson import ObjectId

from werkzeug.security import check_password_hash

from blog import app, mongo, utils
from blog.forms import LoginForm
from blog.utils import auth_route

@app.route('/')
def index():
    posts = mongo.db.posts.find({}).sort([['_id', -1]])[:5]
    return render_template('index.html', posts=posts)

@app.route('/posts')
def posts_search():
    topic = request.args.get('topic', None)
    query_string = request.args.get('q', None)
    try:
        page = int(request.args.get('page', 1))
    except Exception:
        page = 1
    
    query = {}
    if topic and query_string:
        query = { "$and": [
            { 'topics': topic },
            { 'title': { '$regex': '.*' + query_string + '.*'}}
        ]}
    elif topic:
        query = { 'topics': topic }
    elif query_string:
        query = { 'title': { '$regex': '.*' + query_string + '.*'}}

    if query != {}:
        posts = mongo.db.posts.find(query).sort([['_id', -1]])
        posts = posts[(page * 5) - 5:page * 5]
    else:
        posts = {}
    nextPage = utils.build_next_page_url(page, topic=topic, 
                                         query_string=query_string)
    return render_template('posts.html', posts=posts, nextPage=nextPage)

@app.route('/posts/<id>')
def view_post(id):
    post = mongo.db.posts.find_one({'_id': ObjectId(id)})

    if post:
        return render_template('view-post.html', post=post)

@app.route('/posts/delete/<id>')
def delete_post(id):
    post = mongo.db.posts.find_one({'_id': ObjectId(id)})
    return render_template('delete-post.html', post=post)

@app.route('/login', methods=['GET', 'POST'])
def login():
    err = ''
    status = 200
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = mongo.db.users.find_one({'username': form.username.data})
        if user and check_password_hash(user["password"], form.password.data):
            session["username"] = user["username"]
            session["authenticated"] = True
            session["isAdmin"] = user["admin"] if 'admin' in user else None
            return redirect(form.redirect.data)
        else:
            err = "Invalid username or password"
    
    if err:
        status = 401

    redirect_url = request.args.get('redirect', '/')
    return make_response(render_template('login.html', err=err, redirect=redirect_url), status)

@app.route('/logout', methods=['GET'])
@auth_route
def logout():
    session.clear()
    return redirect('/')

@app.route('/post/new', methods=['GET'])
@auth_route
def new_post():
    return render_template('post-editor.html')

@app.route('/posts/edit/<id>', methods=['GET'])
@auth_route
def edit_post(id):
    post = mongo.db.posts.find_one({'_id': ObjectId(id)})
    return render_template('post-editor.html', post=post, edit=True)
    