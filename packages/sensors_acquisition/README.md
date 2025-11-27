
# sensor_acquisition

**Python package to read sensor data and push it to a local database.**

This package collects data from various sensors such as temperature, CO₂, and humidity, and sends it to a local database for storage and further processing.

---

## Features

* Read temperature, CO₂, and humidity from connected sensors
* Validate sensor data using **pydantic** models
* Push data to a local database (PostgreSQL)
* Designed to run on a Raspberry Pi or similar single-board computers
* Easy integration with a backend API
* Gets data from STM32/ESP32 wifi module
---

## Installation

```bash
uv sync --package sensor_acquisition
```

Or install via pip from your workspace venv:

```bash
pip install -e ./sensor_acquisition
```

---

---

## Requirements

* Python 3.13+
* `pydantic`, `paho-mqtt`, `requests` (managed via `pyproject.toml`)

---

## Project Structure

```
sensor_acquisition/
├── src/sensor_acquisition/
│   ├── __init__.py
│   └── __main__.py
├── pyproject.toml
└── README.md
```

---

## License

MIT License

---
