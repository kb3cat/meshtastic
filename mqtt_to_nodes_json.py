import json
import time
import os
import paho.mqtt.client as mqtt

OUTPUT_FILE = os.path.expanduser("~/meshtastic-mqtt/nodes.json")
MQTT_HOST = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "meshtastic/packets"

nodes = {}

def save_nodes():
    data = {
        "updated": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "nodes": list(nodes.values())
    }
    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=2)

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        packet = json.loads(msg.payload.decode())
        decoded = packet.get("decoded", {})
        position = decoded.get("position")

        if position:
            node_id = packet.get("fromId", "unknown")
            nodes[node_id] = {
                "id": node_id,
                "name": node_id,
                "lat": position.get("latitude"),
                "lon": position.get("longitude"),
                "altitude": position.get("altitude"),
                "last_heard": packet.get("rxTime")
            }
            save_nodes()
            print(f"Updated {node_id}")
    except Exception as e:
        print(f"Error: {e}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_HOST, MQTT_PORT, 60)
client.loop_forever()
