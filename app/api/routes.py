import base64
import os

from fastapi import APIRouter, HTTPException

from app.services.camera import capture_jpeg
from app.services.switchbot import SwitchBotClient
from app.services.soil import get_soil_moisture

router = APIRouter()


@router.get("/image")
def get_image(width: int = 800, height: int = 600) -> dict:
    """Capture a frame from the Pi camera and return it as base64."""
    if width <= 0 or height <= 0:
        raise HTTPException(status_code=400, detail="Width and height must be positive")

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
    device_id = os.environ.get("SWITCHBOT_METER_DEVICE_ID")
    if not device_id:
        raise HTTPException(status_code=500, detail="SWITCHBOT_METER_DEVICE_ID not set")
        
    client = SwitchBotClient()
    status = client.get_device_status(device_id)
    
    return {
        "temperature": status.get("temperature"),
        "humidity": status.get("humidity")
    }


@router.get("/sensor/soil")
def get_soil_sensor():
    """Fetch soil moisture data from the connected sensor."""
    return get_soil_moisture()
