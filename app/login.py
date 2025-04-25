from flask import request
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
                print("logged successfully")
                return "logged successfully"
            else:
                print("wrong password")
                return "wrong password"
        else:
            print("user already logged in")
            return "user already logged in"
    else:
        print("user does not exists")
        return "user does not exists"