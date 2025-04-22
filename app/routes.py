from flask import request

from app import getAllUsers
from app.addUser import addUser
from app.login import login
from app.logout import logout
from app.getAllUsers import getAllUsers


def routes(app):
    app.add_url_rule('/login', 'login', login, methods=["POST"])
    app.add_url_rule('/addUser','addUser',addUser, methods=["POST"])
    app.add_url_rule('/logout','logout',logout, methods=["POST"])

    # only for debug purposes, can be used to verify if login procedure works correctly
    app.add_url_rule('/getAllUsers','getAllUsers',getAllUsers)




