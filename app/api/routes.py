import base64

from fastapi import APIRouter, HTTPException

from app.services.camera import capture_jpeg

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
