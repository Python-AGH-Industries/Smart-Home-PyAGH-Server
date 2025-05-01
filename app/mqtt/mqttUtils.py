import paho.mqtt.client as mqtt
import datetime

from ..models import SensorType, Sensor, sensor_types, get_max_per_user
from ..components.flask_app import app
from .addMeasurement import addMeasurement

DATA_TOPIC = "pyagh/smarthome/sensors/data"

TEMPERATURE_SCALING = 10
HUMIDITY_SCALING = 10
PRESSURE_SCALING = 1000
LIGHT_SCALING = 1

def mqtt_connect():
    client_id = f"python-mqtt-{datetime.datetime.now().timestamp()}"
    client = mqtt.Client(
        client_id = client_id,
        protocol = mqtt.MQTTv311,
        clean_session = True,
        reconnect_on_failure = False
    )
    client.on_connect = on_connect
    client.on_message = on_message

    client.reconnect_delay_set(min_delay = 1, max_delay = 120)
    client.enable_logger()

    client.connect("broker.hivemq.com", 1883, 120)
    client.loop_start()
    return client

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(DATA_TOPIC, qos = 0)

# This callback is entered whenever message is received
# on subscribed topic. Callback processes data to a form
# possible to be saved in database
def on_message(client, userdata, msg):
    timestamp = datetime.datetime.now()

    userId = int.from_bytes(msg.payload[0:2], byteorder='little')

    print(f"Received {len(msg.payload)} bytes of data on {timestamp}")
    print(f"User ID: {userId}")

    # Read mqtt data raw values
    temperature_raw = []
    humidity_raw = []
    pressure_raw = []
    light_raw = []
    
    for i in range(6, 12, 2):
        temperature_raw.append(int.from_bytes(
            msg.payload[i: i + 2], 
            byteorder = 'little'
        ))
    
    for i in range(12, 18, 2):
        humidity_raw.append(int.from_bytes(
            msg.payload[i: i + 2],
            byteorder = 'little'
        ))
    
    for i in range(18, 30, 4):
        pressure_raw.append(int.from_bytes(
            msg.payload[i: i + 4],
            byteorder = 'little'
        ))
    
    for i in range(30, 42, 4):
        light_raw.append(int.from_bytes(
            msg.payload[i: i + 4],
            byteorder = 'little'
        ))
    
    # Convert raw values to real ones
    temperature = [x / TEMPERATURE_SCALING for x in temperature_raw]
    humidity = [x / HUMIDITY_SCALING for x in humidity_raw]
    pressure = [x / PRESSURE_SCALING for x in pressure_raw]
    light = [x / LIGHT_SCALING for x in light_raw]

    data = [
        temperature,
        humidity,
        pressure,
        light
    ]

    # Save to DB
    with app.app_context():
        reads_per_user = get_max_per_user(userId)
        for i in range(len(sensor_types)):
            type_id = SensorType.query.filter_by(name = sensor_types[i]).first().id
            sensors = Sensor.query.filter_by(
                type_id = type_id,
                user_id = userId
            ).order_by(Sensor.id).all()
            for j in range(reads_per_user):
                addMeasurement(userId, sensors[j].id, data[i][j])
