from paho.mqtt import client
from paho.mqtt.client import MQTTMessage
from app.settings import Settings, get_settings

import json
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from data_models.schemas import SensorData
from app.db import SessionLocal
from app.db_operations import (
    register_or_update_device,
    insert_sensor_reading,

settings: Settings = get_settings()

class MqttClient:

    def __init__(self):
        # Create a "sensor_data/sensors"new MQTT client instance
        self.client = client.Client()
        # Set the callback for receiving messages
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        
        self.INDEX_DEVICE_REGISTRATION:int = 0
        self.INDEX_DEVICE_DATA_UPDATE:int = 1

        # Connect to the MQTT broker
        self.client.connect(
            host=settings.mqtt_broker_ip,
            port=1883,
            keepalive=60,
        )
        self.client.loop_start()
    
    # Callback for when a message is received
    def on_message(self, client, userdata, msg:MQTTMessage):
        try:
            payload = json.loads(msg.payload.decode())
        except json.JSONDecodeError:
            print("Invalid JSON payload")
        return

        topic = msg.topic

        db: Session = SessionLocal()
        try:
            if topic == settings.mqtt_broker_backend_topics[self.INDEX_DEVICE_REGISTRATION]:
                register_or_update_device(
                    db=db,
                    serial_number=payload["serial_number"],
                    firmware_version=payload.get("firmware_version"),
                    device_type=payload["device_type"],
                    sensors=payload.get("sensors", {}),
                )

            elif topic == settings.mqtt_broker_backend_topics[self.INDEX_DEVICE_DATA_UPDATE]:
                sensor_data = SensorData(
                    **payload,
                    timestamp=datetime.now(timezone.utc),
                )

                insert_sensor_reading(
                    db=db,
                    serial_number=payload["serial_number"],
                    sensor_data=sensor_data,
                )

            else:
                print(f"Received message on unknown topic {topic}")

            db.commit()

    except Exception as e:
        db.rollback()
        print(f"Error processing message: {e}")

    finally:
        db.close()
    
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"Backend Connected to MQTT broker!")
            # Subscribe to all topics in config
            for topic in settings.mqtt_broker_backend_topics:
                print(f"Backen subscribing to topic: {topic}")
                client.subscribe(topic)
        else:
            print(f"Failed to connect, return code {rc}")