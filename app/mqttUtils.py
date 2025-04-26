import paho.mqtt.client as mqtt
import datetime

DATA_TOPIC = "pyagh/smarthome/sensors/data"

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

    client.reconnect_delay_set(min_delay=1, max_delay=120)
    client.enable_logger()  # This helps see what's happening internally

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
    newId = int.from_bytes(msg.payload[2:6], byteorder='little')

    print(f"Received {len(msg.payload)} bytes of data on {timestamp}")
    print(f"User ID: {userId}, Reading ID: {newId}")
    
    print("Temperature values:", end = " ")
    for i in range(6, 12, 2):
        print(
            f"{int.from_bytes(msg.payload[i: i + 2], byteorder = 'little')}",
            end = " "
        )
    print()
    
    print("Humidity values:", end = " ")
    for i in range(12, 18, 2):
        print(
            f"{int.from_bytes(msg.payload[i: i + 2], byteorder = 'little')}",
            end = " "
        )
    print()
    
    print("Pressure values:", end = " ")
    for i in range(18, 30, 4):
        print(
            f"{int.from_bytes(msg.payload[i: i + 4], byteorder = 'little')}",
            end = " "
        )
    print()
    
    print("Light values:", end = " ")
    for i in range(30, 42, 4):
        print(
            f"{int.from_bytes(msg.payload[i: i + 4], byteorder = 'little')}",
            end = " "
        )
    print()
    print()