from flask import request ,jsonify
from app.models import User, Sensor, Measurement
from flask_login import current_user,login_required


@login_required
def readSensorData():
    sensor_id = request.json["sensor_id"]
    data = Measurement.query.filter_by(sensorId = sensor_id).all()
    print(data)
    return "A"
