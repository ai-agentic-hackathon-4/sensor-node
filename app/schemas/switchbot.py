from enum import Enum, IntEnum
from pydantic import BaseModel

class SwitchBotCommand(BaseModel):
    command: str
    parameter: str = "default"
    commandType: str = "command"

class ACMode(IntEnum):
    AUTO = 1
    COOL = 2
    DRY = 3
    FAN = 4
    HEAT = 5

class FanSpeed(IntEnum):
    AUTO = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4

class ACSettings(BaseModel):
    temperature: int
    mode: ACMode
    fan_speed: FanSpeed = FanSpeed.AUTO
    is_on: bool = True

class HumidifierMode(str, Enum):
    AUTO = "auto"
    LOW = "101"
    MEDIUM = "102"
    HIGH = "103"

class HumidifierSettings(BaseModel):
    mode: HumidifierMode
    is_on: bool = True
