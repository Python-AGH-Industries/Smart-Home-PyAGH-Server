from flask import request, jsonify

from .database import db
from app.models import User

def addUser():
    username = request.json["username"]
    password = request.json["password"]
    userplan = request.json["userplan"]

    if User.query.filter_by(username = username).first() is None:
        newUser = User(username = username, userplan = userplan)
        newUser.setPassword(password)
        db.session.add(newUser)
        db.session.commit()
        return jsonify({"message": "User added"}), 200
    else:
        return jsonify({"message": "User already exists"}), 400

