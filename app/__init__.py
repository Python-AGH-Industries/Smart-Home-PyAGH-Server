from .models import User
from .routes import routes
import os

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, logout_user, login_required, current_user, LoginManager

db = SQLAlchemy()
baseDir = os.path.abspath(os.path.dirname(__file__))

def create_app(config_class = "config.Config"):
    app = Flask(__name__, instance_relative_config = True)

    app.config["SQLALCHEMY_DATABASE_URI"] = \
        'sqlite:///' + \
        os.path.join(baseDir, "../database/smartHome.db")
    
    app.secret_key = 'shh,itsSuperSecretKey'
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    routes(app)

    with app.app_context():

        db.create_all()

        return app

