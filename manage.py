#!/usr/bin/env python

from flask_script import Manager
import flask_s3

from werkzeug.security import generate_password_hash

import getpass
import pytest

from blog import app, mongo

manager = Manager(app)

@manager.command
def createuser():
    username = input("Username: ")
    pswd = getpass.getpass("Password: ")
    first_name = input("First name: ")
    last_name = input("Last name: ")

    password = generate_password_hash(pswd)
    document = {
        "username": username,
        "password": password,
        "first_name": first_name,
        "last_name": last_name
    }
 
    mongo.db.users.insert_one(document)
    
@manager.command
def rmuser():
    username = input("Type the username of the user you want to remove: ")
    
    mongo.db.users.delete_one({"username": username})

@manager.command
def s3upload():
    flask_s3.create_all(app)

@manager.command
def test():
    import blog.tests

    # shut up pylint
    blog.tests
    
    pytest.main(["blog/tests.py"])
    
if __name__ == "__main__":
    manager.run()