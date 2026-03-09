import json
import time
import paho.mqtt.client as mqtt
from pubsub import pub
import meshtastic.serial_interface

SERIAL_PORT = "/dev/ttyUSB1"
MQTT_HOST = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "meshtastic/packets"

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
mqtt_client.loop_start()

def on_receive(packet, interface):
    try:
        payload = json.dumps(packet, default=str)
        mqtt_client.publish(MQTT_TOPIC, payload)
        print(f"Published packet from {packet.get('fromId', 'unknown')} to MQTT")
    except Exception as e:
        print(f"Error publishing packet: {e}")

pub.subscribe(on_receive, "meshtastic.receive")

interface = meshtastic.serial_interface.SerialInterface(devPath=SERIAL_PORT)

print(f"Listening on {SERIAL_PORT} and publishing to {MQTT_TOPIC}")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping...")
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
