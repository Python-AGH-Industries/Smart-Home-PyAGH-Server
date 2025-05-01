from flask import request, jsonify
from app.models import User, Sensor
from flask_login import current_user, login_required

@login_required
def getUserSensors():
    type_id = request.json["type_id"]
    user = User.query.filter_by(username = current_user.username).first()

    sensor_data = Sensor.query.filter_by(
        user_id = user.id,
        type_id=type_id
    ).all()

    data = []

    for sensor in sensor_data:
        data.append(sensor.serialize())

    return jsonify({"sensors": data})
