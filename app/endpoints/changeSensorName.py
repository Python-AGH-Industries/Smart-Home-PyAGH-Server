from ..components.database import db
from ..models import User, Sensor
from flask import request, jsonify

def changeSensorName():
    username = request.json["username"]
    oldSensorName = request.json["oldName"]
    newSensorName = request.json["newName"]

    userData = User.query.filter_by(username = username).first()

    if userData is None:
        return jsonify({
            "error": "User not found"
        }), 404
    
    existingSensor = Sensor.query.filter_by(
        user_id = userData.id,
        name = newSensorName
    ).first()

    if existingSensor is not None:
        return jsonify({
            "error": "This name is already taken"
        }), 400
    
    sensorData = Sensor.query.filter_by(
        user_id = userData.id,
        name = oldSensorName
    ).first()

    if sensorData is None:
        return jsonify({
            "error": "Sensor not found"
        }), 404
    
    sensorData.set_name(newSensorName)
    db.session.commit()

    return jsonify({"response": "ok"}), 200
