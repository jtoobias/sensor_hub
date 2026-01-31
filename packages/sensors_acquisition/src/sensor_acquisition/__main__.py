"""Main entry point for sensor data acquisition application."""
import time
from sensor_acquisition.mqtt import MqttClient
from sensor_acquisition.device_manager import DeviceManager

         
def main():
    mqtt_client: MqttClient = MqttClient()
    device_manager: DeviceManager = DeviceManager(mqtt_client=mqtt_client)
    
    while True:
        # Process and store messages
        # print(f"Waiting for messages...{mqtt_client.msg_queue.empty()} {device_manager.devices}")
        if not mqtt_client.msg_queue.empty():
            device_manager.packet_handler(mqtt_client.msg_queue.get(block=False))
        # Change to asynchronous sleep if needed
        time.sleep(1)
        
        # mqtt_client.publish_msg("sensor_device/registration_response",f"ACK_TEST")

if __name__ == "__main__":
    main()