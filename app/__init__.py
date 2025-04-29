from .models import User, init_enums, init_dummy
from .routes import routes
from .mqttUtils import mqtt_connect
from .database import db
from .flask_app import app
import os

from flask_login import LoginManager

baseDir = os.path.abspath(os.path.dirname(__file__))

def create_app():
    db_dir = os.path.join(baseDir, "../database")
    os.makedirs(db_dir, exist_ok = True)

    app.config["SQLALCHEMY_DATABASE_URI"] = \
        'sqlite:///' + \
        os.path.join(baseDir, "../database/smartHome.db")
    
    app.secret_key = 'shh,itsSuperSecretKey'
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    routes(app)

    with app.app_context():
        # Creating and initializing database
        db.create_all()
        init_enums()
        # init_dummy()

        # Connecting to MQTT broker
        mqtt_connect()

        return app

