from .models import UserPlan, SensorType, User
from .routes import routes
from .mqttUtils import mqtt_connect
from .database import db
import os

from flask import Flask
from flask_login import LoginManager

baseDir = os.path.abspath(os.path.dirname(__file__))

def init_enums():
    sensor_types = ["TEMPERATURE", "HUMIDITY", "PRESSURE", "LIGHT"]
    user_plans = [("FREE", 3), ("STANDARD", 6), ("PREMIUM", 9)]

    for type in sensor_types:
        if SensorType.query.filter_by(name = type).first() is None:
            db.session.add(SensorType(name = type))

    for plan, max_number in user_plans:
        if UserPlan.query.filter_by(name = plan).first() is None:
            db.session.add(UserPlan(name = plan, max_per_type = max_number))

    db.session.commit()

def create_app():
    app = Flask(__name__, instance_relative_config = True)

    db_dir = os.path.join(baseDir, "../database")
    os.makedirs(db_dir, exist_ok = True)

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

        # Creating and initializing database
        db.create_all()
        init_enums()

        # Connecting to MQTT broker
        mqtt_connect()

        return app

