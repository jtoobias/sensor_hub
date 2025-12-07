from paho.mqtt import client
from queue import SimpleQueue
import time
import csv
from datetime import datetime
from sensor_acquisition.app_settings import Settings, get_settings
# import yaml

# File to store data
CSV_FILE = "mqtt_data.csv"

settings: Settings = get_settings()

# Load YAML configuration file
# def load_config(file_path="config.yaml"):
#     with open(file_path, "r") as file:
#         return yaml.safe_load(file)

# Create the CSV file and write headers if not exist
with open(CSV_FILE, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "CO2", "TVOC","sdc40_co2","temp","Rhumid"])  # Header

class MqttClient:

    def __init__(self, config: dict):
        # Create a "sensor_data/sensors"new MQTT client instance
        self.client = client.Client()
        print(config)
        # Set the callback for receiving messages
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self.msg_queue = SimpleQueue()

        self.temperature: float = 0.0
        self.pressure: int = 0
        self.co2: int = 0
        self.tvoc: int = 0

        # Connect to the MQTT broker
        self.client.connect(
            host=settings.mqtt_broker_ip,
            port=1883,
            keepalive=60,
        )
        
        
        # Loop forever in another thread to listen for messages
        self.client.loop_start()


    # Callback for when a message is received
    def on_message(self, client, userdata, msg):
        # print(f"Received message on {msg.topic}: {msg.payload.decode()}")
        self.msg_queue.put(msg)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT broker!")

            # Subscribe to the topic
            # self.client.subscribe("sensor_data/sensor")
            # Subscribe to all topics in config
            for topic in settings.mqtt_broker_topics:
                print(f"Subscribing to topic: {topic}")
                client.subscribe(topic)
        else:
            print(f"Failed to connect, return code {rc}")


# if __name__ == "__main__":
#     print("Hello from sensor_acquisition!")
if __name__ == "__main__":
    mqtt_client: MqttClient = MqttClient(config=settings.model_dump())
    while True:
        # Process and store messages
        if not mqtt_client.msg_queue.empty():
            message = mqtt_client.msg_queue.get()
            print(f"CO2,TVOC,co2_scd40(ppm),temp,rh: {message.payload.decode()}")
            # Save message to CSV
            with open(CSV_FILE, mode="a", newline="") as file:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Format timestamp
                writer = csv.writer(file)
                data: list[int] = message.payload.decode().split(",")
                writer.writerow([timestamp, data[0], data[1],data[2], int(data[3])/10, int(data[4])/10])
            # Note: Do further processing here, like saving to database
        time.sleep(1)
