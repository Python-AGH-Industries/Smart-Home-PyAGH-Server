from .database import db
from .models import User, Sensor, Measurement

def addMeasurement(mqttDataPacket):
    userId = mqttDataPacket.userId
    sensorId = mqttDataPacket.sensorId
    time = mqttDataPacket.time
    date = mqttDataPacket.date
    value = mqttDataPacket.value

    if User.query.filter_by(id = userId).first() is None:
        return
    
    if Sensor.query.filter_by(id = sensorId).first() is None:
        return
    
    newMeasurement = Measurement(
        sensorId = sensorId,
        measurementTime = time,
        measurementDate = date,
        measurementValue = value
    )

    db.session.add(newMeasurement)
    db.session.commit()
