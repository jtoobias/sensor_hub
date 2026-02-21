"""Handles sensor devices classes"""
from pydantic import BaseModel, Field, ConfigDict
from data_models.models import SensorDevice,SensorData,SENSOR_ID_MAP
from data_models.gobal_constants import MqttTopics
from paho.mqtt.client import MQTTMessage
from sensor_acquisition.mqtt import MqttClient
from datetime import datetime, timezone
from typing import Any, Dict, Callable
from loguru import logger


class DeviceManager(BaseModel):
    devices: dict[int,SensorDevice] = Field(default_factory=dict)
    uuids: set[int] = Field(default_factory=set)
    mqtt_client: MqttClient = Field(default_factory=MqttClient) 
    packet_handler: Dict[str,Callable[[MQTTMessage],bool]] = Field(default_factory=dict) 
    
    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )
    
    def model_post_init(self, context: Any) -> None:
        self.packet_handler: Dict[str,Callable[[MQTTMessage],bool]] = {
            MqttTopics.REMOTE_DEVICE_REGISTRATION: self._on_sensor_device_registration,
            MqttTopics.REMOTE_DEVICE_DATA: self._on_sensor_data_msg, 
        }
        return super().model_post_init(context)
                    
    @staticmethod
    def build_ack_packet(serial_number:int) -> str:
        return f"A,{serial_number}"
    
    @staticmethod
    def build_nack_packet(serial_number:int) -> str:
        return f"N,{serial_number}"
    
    def build_sensor_data(
        self,
        payload: list[int],
        sensor_ids: list[int] | None,
    ) -> SensorData:
        """
        Build SensorData from payload using registered sensor IDs.
        """

        data: dict[str, Any] = {}
        if sensor_ids is None:
            # ToDo: Will need to check pre-determined list of sensor IDs here and tell it to re-register in response
            return SensorData(
                serial_number=payload[0],
                rssi=int(payload[1]),
                battery_voltage=float(payload[2])/1000.0,
                timestamp=datetime.now(timezone.utc),
            )
        for sensor_id, raw_value in zip(sensor_ids, payload[3:]):
            field_name = SENSOR_ID_MAP.get(sensor_id)

            if not field_name:
                continue  # unknown sensor, ignore safely

            # Potientially move this to seperate functions.
            if field_name in {"temperature", "humidity"}:
                data[field_name] = raw_value / 10.0
            else:
                data[field_name] = raw_value

        return SensorData(
            serial_number=payload[0],
            rssi=int(payload[1]),
            battery_voltage=float(payload[2])/1000.0,
            **data,
            timestamp=datetime.now(timezone.utc),
        )
        
        
    def _on_sensor_data_msg(self,msg:MQTTMessage):
        data_parts = msg.payload.decode().split(",")
        if len(data_parts) >= 3:
            serial_number: int = int(data_parts[0])
            if serial_number not in self.devices:
                self.uuids.add(serial_number)
                logger.info(f"Registering new device with serial number: {serial_number}")
                #Sensor device registering
                self.devices[serial_number] = (SensorDevice(
                    serial_number=serial_number,
                    firmware_version=f"{data_parts[1]}.{data_parts[2]}.{data_parts[3]}",
                    device_type=int(data_parts[4]),
                    sensor_ids=[int(id) for id in data_parts[5:]],
                ))           
                logger.info(f"Device {serial_number} now registered.")
                self.mqtt_client.publish_msg(MqttTopics.REMOTE_DEVICE_REGISTRATION_RESPONSE,self.build_ack_packet(serial_number))
            else:
                logger.info(f"Device {serial_number} already registered. Resending ACK.")
                self.mqtt_client.publish_msg(MqttTopics.REMOTE_DEVICE_REGISTRATION_RESPONSE,self.build_ack_packet(serial_number))
            return True
        else:
            serial_number: int = int(data_parts[0])
            logger.info(f"Device {serial_number}? {data_parts} Data message length {len(data_parts)} incorrect.")
            self.mqtt_client.publish_msg(MqttTopics.REMOTE_DEVICE_REGISTRATION_RESPONSE,self.build_nack_packet(serial_number))
        return False
    
    def _on_sensor_device_registration(self,msg:MQTTMessage) -> bool:
        #ToDo: Check if it is rquired to ack data reception
        data_parts = msg.payload.decode().split(",")
        if len(data_parts) >= 2:
            payload: list[int] = [int(value) for value in data_parts]
            serial_number: int = payload[0]
            device = self.devices.get(serial_number)
            if not device:
                logger.info(f"Unregistered device {serial_number} sent data.")
                return False
            sensor_data:SensorData = self.build_sensor_data(payload=payload,
                                                        sensor_ids=device.sensor_ids
                                                        )
            
            #ToDo: Update data base by sending mqtt to backend for data
            logger.info(f"Parsed Sensor Data: {sensor_data}")
            self.mqtt_client.publish_msg(MqttTopics.REMOTE_DEVICE_DATA_RESPONSE,self.build_ack_packet(serial_number))
            return True
        else:
            serial_number: int = int(data_parts[0])
            logger.info(f"Device {serial_number}? {data_parts} Data message length {len(data_parts)} incorrect.")
            self.mqtt_client.publish_msg(MqttTopics.REMOTE_DEVICE_DATA_RESPONSE,self.build_nack_packet(serial_number))
        return False
