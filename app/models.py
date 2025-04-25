from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from .database import db

# enum table holding possible sensor types
class SensorType(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(10), nullable = False)

    def __repr__(self):
        return f"<Sensor Type {self.name}>"

# enum table holding possible user subscription plans
class UserPlan(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(10), nullable = False)
    max_per_type = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f"<User Plan {self.name}>"

# user database
class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), nullable = False)
    password = db.Column(db.String(200), nullable = False)
    userplan = db.Column(db.Integer, db.ForeignKey('user_plan.id'), nullable = False)
    sensors = db.relationship('Sensor', backref = 'owner', lazy = True)

    def setPassword(self, password):
        self.password = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User {self.id} - {self.username}>"

# sensors database
class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    typeId = db.Column(db.Integer, db.ForeignKey('sensor_type.id'), nullable = False)
    ownerId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    name = db.Column(db.String(20), nullable = False) # user given name
    sensors = db.relationship('Measurement', backref = 'sensor', lazy = True)

    def __repr__(self):
        return f"<Sensor {self.id} - OwnerId:{self.ownerId}>"

# sensor reading database
class Measurement(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    sensorId = db.Column(db.Integer, db.ForeignKey('sensor.id'), nullable = False)
    measurementTime = db.Column(db.Time, nullable = False)
    measurementDate = db.Column(db.Date, nullable = False)
    measurementValue = db.Column(db.Integer, nullable = True)

    def __repr__(self):
        return f"<Sensor {self.sensorId} - Value:{self.measurementValue}>"
