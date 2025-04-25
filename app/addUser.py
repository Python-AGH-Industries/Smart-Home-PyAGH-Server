from flask import request, jsonify
from werkzeug.security import generate_password_hash

from .database import db
from app.models import User

def addUser():
    username = request.json["username"]
    password = request.json["password"]

    if User.query.filter_by(username = username).first() is None:
        newUser = User(username = username)
        newUser.setPassword(password)
        db.session.add(newUser)
        db.session.commit()
        return jsonify({"message": "User added"}), 201
    else:
        return jsonify({"message": "User already exists"}), 400

