from flask import request
from werkzeug.security import generate_password_hash

from . import db
from app.models import User


def addUser():


    username = request.json["username"]
    password = request.json["password"]

    if User.query.filter_by(username=username).first() is None:
        newUser = User(username = username)
        newUser.setPassword(password)
        db.session.add(newUser)
        db.session.commit()
        return "user added"
    else:
        users = User.query.all()
        for user in users:
            print(f"ID: {user.id}, Name: {user.username}")

        return "user already exists"

