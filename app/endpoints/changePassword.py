from flask import request, jsonify
from flask_login import current_user
from ..models import User
from ..components.database import db

def changePassword():
    username = request.json["username"]
    newPassword = request.json["newPassword"]
    oldPassword = request.json["oldPassword"]

    userData = User.query.filter_by(username = username).first()

    if userData is not None:
        if not current_user.is_authenticated:
            if userData.check_password(oldPassword):
                userData.set_password(newPassword)
                db.session.commit()
                return jsonify({
                    "respone": "Password changed",
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