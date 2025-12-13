from sqlalchemy import Column, Integer, Float, DateTime,ForeignKey,JSON,String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db import Base
from datetime import datetime, timezone
# Device_types -> Device -> SensorReadings

# How it fits together
# Device registration example (backend flow)
# ESP32 connects → sends serial_number + type_name
# Backend checks devices table:
# If new → create device row, link to device_types
# If exists → update last_seen
# When sensor data arrives → insert into sensor_readings linked by device_id

class DeviceType(Base):
    __tablename__ = "device_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String)
    expected_sensors: Mapped[JSON] = mapped_column(JSON)  # can store sensor names and types
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    

    devices = relationship("Device", back_populates="device_type")

class Device(Base):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(primary_key=True)
    serial_number: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    device_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    firmware_version: Mapped[str] = mapped_column(String, nullable=True)
    first_seen: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    last_seen: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    device_type = relationship("DeviceType", back_populates="devices")    
    # One-to-many relationship: this device → its readings
    readings = relationship(
        "SensorReading",
        back_populates="device",
        cascade="all, delete-orphan"
    )

#Define database schema.
class SensorReading(Base):
    """Table storing raw sensor readings."""
    __tablename__ = "sensor_readings"

    id: Mapped[int] = mapped_column(primary_key=True)
    device_id: Mapped[int] = mapped_column(Integer, ForeignKey("devices.id"), index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    temperature: Mapped[float] = mapped_column(Float, nullable=True,default=None)
    humidity: Mapped[float] = mapped_column(Float, nullable=True,default=None)
    pressure: Mapped[float] = mapped_column(Float, nullable=True,default=None)
    co2_ppm: Mapped[float] = mapped_column(Float, nullable=True,default=None)

    battery_voltage: Mapped[float] = mapped_column(Float)
    rssi: Mapped[int] = mapped_column(Integer)
    device = relationship("Device", back_populates="readings")

