import base64
import os

from fastapi import APIRouter, HTTPException

from app.services.camera import capture_jpeg
from app.services.switchbot import SwitchBotClient
from app.services.soil import get_soil_moisture
from app.services.bh1750 import get_lux
from app.services.pump import pour_water

from app.schemas.switchbot import ACSettings, HumidifierSettings, PlugMiniSettings
from app.schemas.pump import PumpRequest


router = APIRouter()
print("DEBUG: Routes module loaded. Pump route should be registered.")


@router.get("/image")
def get_image(width: int = None, height: int = None) -> dict:
    """Capture a frame from the Pi camera and return it as base64."""
    if width is not None and width <= 0:
        raise HTTPException(status_code=400, detail="Width must be positive")
    if height is not None and height <= 0:
        raise HTTPException(status_code=400, detail="Height must be positive")

    image_bytes = capture_jpeg(width=width, height=height)
    encoded = base64.b64encode(image_bytes).decode("ascii")

    return {
        "width": width,
        "height": height,
        "format": "jpeg",
        "data_base64": encoded,
    }


@router.get("/sensor/meter")
def get_meter_sensor():
    """Fetch temperature and humidity from the configured Switchbot meter."""
    from app.core.config import get_settings
    settings = get_settings()
    device_id = settings.SWITCHBOT_METER_DEVICE_ID
    if not device_id:
        raise HTTPException(status_code=500, detail="SWITCHBOT_METER_DEVICE_ID not set")
        
    client = SwitchBotClient()
    status = client.get_device_status(device_id)
    
    return {
        "temperature": status.get("temperature"),
        "humidity": status.get("humidity")
    }

@router.get("/sensor/air-conditioner")
def get_ac_status():
    """Fetch status of the Air Conditioner."""
    from app.core.config import get_settings
    settings = get_settings()
    device_id = settings.SWITCHBOT_AC_DEVICE_ID
    if not device_id:
        raise HTTPException(status_code=500, detail="SWITCHBOT_AC_DEVICE_ID not set")
        
    client = SwitchBotClient()
    status = client.get_device_status(device_id)
    return status

@router.get("/sensor/humidifier")
def get_humidifier_status():
    """Fetch status of the Humidifier."""
    from app.core.config import get_settings
    settings = get_settings()
    device_id = settings.SWITCHBOT_HUMIDIFIER_DEVICE_ID
    if not device_id:
        raise HTTPException(status_code=500, detail="SWITCHBOT_HUMIDIFIER_DEVICE_ID not set")
        
    client = SwitchBotClient()
    status = client.get_device_status(device_id)
    return status


@router.get("/sensor/soil")
def get_soil_sensor():
    """Fetch soil moisture data from the connected sensor."""
    return get_soil_moisture()


@router.get("/sensor/bh1750")
def get_bh1750_sensor():
    """Fetch lux data from the BH1750 sensor."""
    return get_lux()
    


@router.post("/control/air-conditioner/settings")
def control_ac_settings(settings: ACSettings):
    """
    Control AC with specific settings (Temp, Mode, Fan).
    Command: setAll
    Parameter: {temperature},{mode},{fan_speed},{power_state}
    """
    from app.core.config import get_settings
    settings_conf = get_settings()
    device_id = settings_conf.SWITCHBOT_AC_DEVICE_ID
    
    client = SwitchBotClient()
    return client.control_ac_settings(settings, device_id)

@router.post("/control/humidifier/settings")
def control_humidifier_settings(settings: HumidifierSettings):
    """
    Control Humidifier modes.
    """
    from app.core.config import get_settings
    settings_conf = get_settings()
    device_id = settings_conf.SWITCHBOT_HUMIDIFIER_DEVICE_ID
    client = SwitchBotClient()
    return client.control_humidifier_settings(settings, device_id)


@router.post("/control/pump")
def control_pump(request: PumpRequest):
    """
    Control Water Pump.
    """
    return pour_water(request.volume_ml)

@router.post("/control/plug-mini/settings")
def control_plug_mini_settings(settings: PlugMiniSettings):
    """
    Control Plug Mini (Power on/off only).
    """
    from app.core.config import get_settings
    conf = get_settings()
    device_id = conf.SWITCHBOT_PLUG_MINI_DEVICE_ID
    if not device_id:
        raise HTTPException(status_code=500, detail="SWITCHBOT_PLUG_MINI_DEVICE_ID not set")
    
    client = SwitchBotClient()
    return client.control_plug_mini(settings, device_id)
