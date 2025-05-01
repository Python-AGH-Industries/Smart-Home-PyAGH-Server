from ..components.database import db
from ..models import User, Sensor, Measurement
from datetime import datetime

def addMeasurement(userId, sensorId, value):
    if User.query.filter_by(id = userId).first() is None:
        return
    
    if Sensor.query.filter_by(id = sensorId).first() is None:
        return
    
    now = datetime.now()
    
    newMeasurement = Measurement(
        sensorId = sensorId,
        measurementTime = now.time(),
        measurementDate = now.date(),
        measurementValue = value
    )

    print(f"Adding new data to sensor {newMeasurement.sensorId}")

    db.session.add(newMeasurement)
    db.session.commit()
