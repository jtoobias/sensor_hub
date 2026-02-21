from enum import StrEnum

class MqttTopics(StrEnum):
    # Sensor device -> Sensor_acquisition
    REMOTE_DEVICE_REGISTRATION = "sensor_device/registration"
    REMOTE_DEVICE_REGISTRATION_RESPONSE = "sensor_device/registration_response"
    REMOTE_DEVICE_DATA = "sensor_device/data"
    REMOTE_DEVICE_DATA_RESPONSE = "sensor_device/data_response"
    
    # Sensor_acquisition -> ANY
    DEVICE_BACKEND_REGISTRATION = "sensor_acquisition/device_registration"
    DEVICE_BACKEND_DATA = "sensor_acquisition/device_data"