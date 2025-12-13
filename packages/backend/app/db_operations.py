# app/db_operations.py
from sqlalchemy import Column, Integer, Float, DateTime,ForeignKey,JSON,String
from datetime import datetime,timezone
from sqlalchemy.orm import Session
from .models import DeviceType, Device, SensorReading
from .db import SessionLocal

# -------------------------
# Session helper
# -------------------------
def get_session() -> Session:
    """Get a new database session."""
    return SessionLocal()

# -------------------------
# DeviceType CRUD
# -------------------------
def create_device_type(name: str, expected_sensors: dict, description: str | None = None):
    """Create a new device type."""
    session = get_session()
    try:
        dtype = DeviceType(
            name=name,
            expected_sensors=expected_sensors,
            description=description
        )
        session.add(dtype)
        session.commit()
        return dtype
    finally:
        session.close()

def get_device_type(name: str):
    """Fetch a device type by name."""
    session = get_session()
    try:
        return session.query(DeviceType).filter_by(name=name).first()
    finally:
        session.close()

def delete_device_type(name: str):
    """Delete a device type by name."""
    session = get_session()
    try:
        dtype = session.query(DeviceType).filter_by(name=name).first()
        if not dtype:
            return False
        session.delete(dtype)
        session.commit()
        return True
    finally:
        session.close()

# -------------------------
# Device CRUD
# -------------------------
def register_device(serial_number: str, device_type_name: str, firmware_version: str | None = None):
    """Register a new device or update last_seen if it exists."""
    session = get_session()
    try:
        dtype = session.query(DeviceType).filter_by(name=device_type_name).first()
        if not dtype:
            raise ValueError(f"DeviceType '{device_type_name}' does not exist")

        device: Device = session.query(Device).filter_by(serial_number=serial_number).first()
        if device:
            # Update last_seen
            device.last_seen = datetime.now(timezone.utc)
        else:
            # Create new device
            device = Device(
                serial_number=serial_number,
                device_type=dtype,
                firmware_version=firmware_version,
                last_seen=datetime.now(timezone.utc)
            )
            session.add(device)

        session.commit()
        return device
    finally:
        session.close()

def get_device(serial_number: str):
    """Fetch a device by serial number."""
    session = get_session()
    try:
        return session.query(Device).filter_by(serial_number=serial_number).first()
    finally:
        session.close()

def delete_device(serial_number: str):
    """Delete a device and all its readings."""
    session = get_session()
    try:
        device = session.query(Device).filter_by(serial_number=serial_number).first()
        if not device:
            return False
        session.delete(device)
        session.commit()
        return True
    finally:
        session.close()

def update_last_seen(serial_number: str):
    """Update last_seen timestamp for a device."""
    session = get_session()
    try:
        device = session.query(Device).filter_by(serial_number=serial_number).first()
        if not device:
            raise ValueError(f"Device '{serial_number}' not found")
        device.last_seen = datetime.utcnow()
        session.commit()
        return device
    finally:
        session.close()

# -------------------------
# SensorReading CRUD
# -------------------------
def insert_sensor_reading(serial_number: str, data: dict):
    """
    Insert a new sensor reading and update the device's last_seen.
    Data dict keys: temperature, humidity, pressure, co2_ppm, battery_voltage, rssi
    """
    session = get_session()
    try:
        device = session.query(Device).filter_by(serial_number=serial_number).first()
        if not device:
            raise ValueError(f"Device '{serial_number}' not registered")

        # Update last_seen
        device.last_seen = datetime.utcnow()

        # Create new reading
        reading = SensorReading(
            device=device,
            timestamp=datetime.utcnow(),
            temperature=data.get("temperature"),
            humidity=data.get("humidity"),
            pressure=data.get("pressure"),
            co2_ppm=data.get("co2_ppm"),
            battery_voltage=data.get("battery_voltage"),
            rssi=data.get("rssi")
        )
        session.add(reading)
        session.commit()
        return reading
    finally:
        session.close()

def get_readings_for_device(serial_number: str, limit: int = 100):
    """Fetch the last N readings for a device."""
    session = get_session()
    try:
        device = session.query(Device).filter_by(serial_number=serial_number).first()
        if not device:
            return []
        return session.query(SensorReading)\
            .filter_by(device_id=device.id)\
            .order_by(SensorReading.timestamp.desc())\
            .limit(limit).all()
    finally:
        session.close()

def delete_reading(reading_id: int):
    """Delete a sensor reading by ID."""
    session = get_session()
    try:
        reading = session.query(SensorReading).filter_by(id=reading_id).first()
        if not reading:
            return False
        session.delete(reading)
        session.commit()
        return True
    finally:
        session.close()
