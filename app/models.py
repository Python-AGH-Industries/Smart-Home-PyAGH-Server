from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import event

from .database import db

# enum table holding possible sensor types
class SensorType(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable = False)

    def __repr__(self):
        return f"<Sensor Type {self.name}>"

# enum table holding possible user subscription plans
class UserPlan(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable = False)
    max_per_type = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f"<User Plan {self.name}>"

# user database
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), nullable = False, unique = True)
    password = db.Column(db.String(200), nullable = False)
    userplan_id = db.Column(
        db.Integer,
        db.ForeignKey('user_plan.id'),
        nullable = False
    )
    
    # Relationship to Sensor (1 user → many sensors)
    sensors = db.relationship(
        'Sensor', 
        backref = 'owner', 
        lazy = True,
        cascade = 'all, delete-orphan'
    )

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User {self.id}: {self.username}>"

# Event listener to create sensors after user creation
# Each user the amount of person based on their plan
@event.listens_for(User, 'after_insert')
def create_default_sensors(mapper, connection, target):
    userPlan = target.userplan_id
    max_per_user = UserPlan.query.filter_by(id = userPlan).first().max_per_type
    bases = [("T", 1), ("H", 2), ("P", 3), ("L", 4)]
    defaults = []

    for baseName, typeId in bases:
        for i in range(1, max_per_user + 1):
            defaults.append((baseName + str(i), typeId))

    sensor_table = Sensor.__table__
    connection.execute(
        sensor_table.insert(),
        [{
            'name': name,
            'type_id': typeId,
            'user_id': target.id
        } for name, typeId in defaults]
    )

# sensors
class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    type_id = db.Column(
        db.Integer,
        db.ForeignKey('sensor_type.id'),
        nullable = False
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable = False
    )
    
    name = db.Column(db.String(20), nullable = False) 
    
    # Relationship to Measurement (1 sensor → many measurements)
    measurements = db.relationship(
        'Measurement',
        backref='sensor', 
        lazy=True,
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f"<Sensor {self.id}: {self.name} (User {self.user_id})>"

# sensor reading database
class Measurement(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    sensorId = db.Column(db.Integer, db.ForeignKey('sensor.id'), nullable = False)
    measurementTime = db.Column(db.Time, nullable = False)
    measurementDate = db.Column(db.Date, nullable = False)
    measurementValue = db.Column(db.Integer, nullable = True)

    def __repr__(self):
        return f"<Sensor {self.sensorId} - Value:{self.measurementValue}>"

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
    
def init_dummy():
    freePlan = UserPlan.query.filter_by(name = "FREE").first()
    premiumPlan = UserPlan.query.filter_by(name = "PREMIUM").first()

    if freePlan is None or premiumPlan is None:
        print("Plan not found")
        return

    usr = User(
        username = "Arima",
        userplan_id = freePlan.id
    )
    usr.set_password("aaa")

    usr2 = User(
        username = "Areczek",
        userplan_id = premiumPlan.id
    )
    usr2.set_password("bbb")

    db.session.add(usr)
    db.session.add(usr2)

    db.session.commit()