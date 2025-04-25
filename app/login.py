from flask import request, jsonify
from flask_login import login_user, current_user

from app.models import User

def login():
    username = request.json["username"]
    password = request.json["password"]
    userData = User.query.filter_by(username = username).first()

    if userData is not None:
        if not current_user.is_authenticated:
            if userData.checkPassword(password):
                login_user(userData)
                return jsonify({"message": "Logged successfully"}), 200
            else:
                return jsonify({"message": "Wrong password"}), 400
        else:
            return jsonify({"message": "User is already logged in"}), 400
    else:
        return jsonify({"message": "User does not exist"}), 400