"""Main entry point for sensor data acquisition application."""
import time
from sensor_acquisition.mqtt import MqttClient,MQTTMessage
from sensor_acquisition.device_manager import DeviceManager
from loguru import logger
from typing import Callable

def setup_logger():
    """Setup the logger configuration."""
    logger.add(
        "sensor_acquisition.log",
        rotation="10 MB",  # Rotate log file after it reaches 10 MB
        retention="5 days",  # Keep logs for 5 days
        compression="zip",  # Compress rotated logs
        level="INFO",  # Set the logging level
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    )

def main():
    mqtt_client: MqttClient = MqttClient()
    device_manager: DeviceManager = DeviceManager(mqtt_client=mqtt_client)
    setup_logger()
    while True:
        # Process and store messages
        # print(f"Waiting for messages...{mqtt_client.msg_queue.empty()} {device_manager.devices}")
        if not mqtt_client.msg_queue.empty():
            msg: MQTTMessage = mqtt_client.msg_queue.get(block=False)
            handler = device_manager.packet_handler.get(msg.topic)
            if handler is None:
                logger.warning(f"Topic: {msg.topic} Not handled")
              
            elif not handler(msg):
                logger.warning(f"Handling of Topic: {msg.topic} Failed")
        # Change to asynchronous sleep if needed
        time.sleep(1)

if __name__ == "__main__":
    main()