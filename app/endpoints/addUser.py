from flask import request, jsonify

from ..components.database import db
from app.models import User

def addUser():
    username = request.json["username"]
    password = request.json["password"]
    userplan = request.json["userplan"]

    if User.query.filter_by(username = username).first() is None:
        newUser = User(username = username, userplan_id = userplan)
        newUser.set_password(password)
        db.session.add(newUser)
        db.session.commit()
        return jsonify({"message": "User added"}), 200
    else:
        return jsonify({"error": "User already exists"}), 400

