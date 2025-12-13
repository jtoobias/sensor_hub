"""Schemas for sensor data validation and serialization."""
from pydantic import BaseModel

class SensorDevice(BaseModel):
    firmware_version: str
    serial_number: str
    device_type: int

class SensorData(SensorDevice):
    temperature: None | float
    humidity: None | float
    pressure: None | float
    co2_ppm: None | float
    battery_voltage: None | float
    rssi: None | int