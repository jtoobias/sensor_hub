This repo is designed to gather, store and provide sensor data


## Message structures
Sensor Device = SD
Base Sensor Acquisition = BSA
Base Backend = BB

Sender: Any
Receiver: Any
Name: ACK
Topic: Any
Packet Style: Byte
Packet structure: A,uuid

Sender: Any
Receiver: Any
Name: NACK
Topic: Any
Packet Style: Byte
Packet structure: N,uuid

Sender: SD
Receiver: Base
Name: Registration
Topic: "sensor_device/registration"
Packet Style: Byte
Packet structure: uuid, FW_MAJOR, FW_MINOR, FW_PATCH, DEVICE_TYPE

Sender: SD
Receiver: Base
Name: Sensor_data
Topic: "sensor_device/data"
Packet Style: Byte
Packet structure: uuid,RSSI,battery_voltage,co2,voltile_gas,temperature,humidity

Sender: Base
Receiver: SD
Name: Sensor_data
Topic: "sensor_device/data_response"
Packet Style: Byte
Packet structure: "ACK"

Sender: BSA
Receiver: BB
Name: Device Registration Storage
Topic: "sensor_acquisition/device_registration"
Packet Style: JSON
Packet structure: uuid, FW_MAJOR, FW_MINOR, FW_PATCH, DEVICE_TYPE

Sender: BSA
Receiver: BB
Name: Device Data Storage
Topic: "sensor_acquisition/device_data"
Packet Style: JSON
Packet structure: "Sensor_data"

## Todo
Message structures