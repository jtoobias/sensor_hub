from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache

class Settings(BaseSettings):
    database_url: str = ""
    # MQTT configuration
    mqtt_broker_ip: str = "192.168.178.181"
    mqtt_broker_username: str = ""
    mqtt_broker_password: str = ""
    mqtt_port: int = 1883
    mqtt_broker_backend_topics: list[str] = Field(default_factory=lambda: ["backend/readings_update",
                                                                            "backend/device_registration"])

    class Config:
        env_file = "../.env"


# LRU cached getter for settings
@lru_cache()
def get_settings() -> Settings:
    """
    Retrieve the application settings.
    This function is cached so that the same Settings instance is reused.
    """
    return Settings()