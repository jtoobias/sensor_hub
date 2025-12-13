# app/schemas.py
from pydantic import BaseModel

class SensorData(BaseModel):
    temperature: None | float
    humidity: None | float
    pressure: None | float
    co2_ppm: None | float
    battery_voltage: None | float
    rssi: None | int
