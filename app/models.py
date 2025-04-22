from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_manager

from . import db


# user database
class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    def setPassword(self, password):
        self.password = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User {self.id} - {self.username}>"



# sensors database
class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ownerId = db.Column(db.Integer,nullable=False)
    roomId = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String(50), nullable=False)
    def __repr__(self):
        return f"<Sensor {self.id} - OwnerId:{self.ownerId}>"


# sensor reading database
class Measurement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensorId = db.Column(db.Integer,nullable=False)
    measurementTime = db.Column(db.Time,nullable=False)
    measurementDate = db.Column(db.Date,nullable=False)
    measurementValue = db.Column(db.Integer,nullable=True)
    def __repr__(self):
        return f"<Sensor {self.sensorId} - Value:{self.measurementValue}>"


