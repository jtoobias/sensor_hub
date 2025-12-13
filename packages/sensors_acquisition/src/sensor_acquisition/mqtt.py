from paho.mqtt import client
from paho.mqtt.client import MQTTMessage
from queue import SimpleQueue
from sensor_acquisition.app_settings import Settings

class MqttClient:

    def __init__(self, mqtt_settings: Settings):
        # Create a "sensor_data/sensors"new MQTT client instance
        self.client = client.Client()
        self.msg_queue:SimpleQueue[MQTTMessage] = SimpleQueue()
        self.settings = mqtt_settings
        # Set the callback for receiving messages
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect

        # Connect to the MQTT broker
        self.client.connect(
            host=self.settings.mqtt_broker_ip,
            port=1883,
            keepalive=60,
        )
        
        self.client.loop_start()
    
    # Callback for when a message is received
    def on_message(self, client, userdata, msg:MQTTMessage):
        # print(f"Received message on {msg.topic}: {msg.payload.decode()}")
        self.msg_queue.put(msg)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT broker!")
            # Subscribe to all topics in config
            for topic in self.settings.mqtt_broker_topics:
                print(f"Subscribing to topic: {topic}")
                client.subscribe(topic)
        else:
            print(f"Failed to connect, return code {rc}")