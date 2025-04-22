from flask import request

from app.addUser import addUser
from app.login import login
from app.logout import logout


def routes(app):
    app.add_url_rule('/login', 'login', login, methods=["POST"])
    app.add_url_rule('/addUser','addUser',addUser, methods=["POST"])
    app.add_url_rule('/logout','logout',logout, methods=["POST"])




