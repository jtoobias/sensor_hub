"""Schemas for sensor data validation and serialization."""
from pydantic import BaseModel
from datetime import datetime, timezone
from enum import IntEnum

SENSOR_ID_MAP = {
    1: "temperature",
    2: "humidity",
    3: "co2_ppm",
    4: "tvoc_ppb",
    5: "pressure",
    # add more as needed
}

class DeviceTypes(IntEnum):
    AIR_QUALITY_SENSOR = 1
    WEATHER_STATION = 2

class SensorDevice(BaseModel):
    """ Example device registration payload:{
        "serial_number": "ESP32_001",
        "firmware_version": "1.0.3",
        "device_type": 1,
        "sensor_ids": [1, 2, 3]
        }
    """
    firmware_version: str
    serial_number: int
    device_type: int                        # Shows the devices is purpose, 1=air quality, 2=weather station etc.
    sensor_ids: list[int] | None = None        # List of sensor IDs present on the device
    

class SensorData(BaseModel):
    serial_number: int
    timestamp: None | datetime = None
    temperature: None | float = None
    humidity: None | float = None
    air_pressure: None | float = None
    tvoc_ppb: None | float = None
    co2_ppm: None | float = None
    battery_voltage: None | float = None
    rssi: None | int = None