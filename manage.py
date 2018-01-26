#!/usr/bin/env python

from flask_script import Manager

from werkzeug.security import generate_password_hash

import getpass

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
    
if __name__ == "__main__":
    manager.run()