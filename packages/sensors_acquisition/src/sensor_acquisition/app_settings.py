from functools import lru_cache
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    # # Database configuration
    # db_host: str = Field("localhost", env="DB_HOST")
    # db_port: int = Field(5432, env="DB_PORT")
    # db_user: str = Field("user", env="DB_USER")
    # db_password: str = Field("password", env="")
    # db_name: str = Field("sensor_data", env="")
    
    # MQTT configuration
    mqtt_broker_ip: str = ""
    mqtt_broker_username: str = ""
    mqtt_broker_password: str = ""
    mqtt_port: int = 1883
    
    # Sensor options
    # sample_interval: float = Field(5.0, env="SAMPLE_INTERVAL")  # seconds

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# LRU cached getter for settings
@lru_cache()
def get_settings() -> Settings:
    """
    Retrieve the application settings.
    This function is cached so that the same Settings instance is reused.
    """
    return Settings()
