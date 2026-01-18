import os
from functools import lru_cache

class Settings:
    def __init__(self):
        self.SWITCHBOT_TOKEN: str = os.environ.get("SWITCHBOT_TOKEN", "")
        self.SWITCHBOT_SECRET: str = os.environ.get("SWITCHBOT_SECRET", "")
        self.SWITCHBOT_METER_DEVICE_ID: str = os.environ.get("SWITCHBOT_METER_DEVICE_ID", "")
        self.SWITCHBOT_AC_DEVICE_ID: str = os.environ.get("SWITCHBOT_AC_DEVICE_ID", "")
        self.SWITCHBOT_HUMIDIFIER_DEVICE_ID: str = os.environ.get("SWITCHBOT_HUMIDIFIER_DEVICE_ID", "")

@lru_cache()
def get_settings() -> Settings:
    return Settings()
