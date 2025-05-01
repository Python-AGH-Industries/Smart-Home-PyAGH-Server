from flask import request, jsonify
from flask_login import login_user, current_user

from app.models import User

def login():
    username = request.json["username"]
    password = request.json["password"]
    userData = User.query.filter_by(username = username).first()
    if userData is not None:
        if not current_user.is_authenticated:
            if userData.check_password(password):
                login_user(userData)
                print(userData.is_authenticated)
                print(userData.get_id())

                return jsonify({
                    "message": "Logged successfully",
                    "success": True
                }), 200
            else:
                return jsonify({
                    "error": "Wrong password",
                    "success": False
                }), 400
        else:
            return jsonify({
                "error": "User is already logged in",
                "success": False
            }), 400
    else:
        return jsonify({
            "error": "User does not exist",
            "success": False
        }), 400