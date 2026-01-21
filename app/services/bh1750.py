import logging
import os

logger = logging.getLogger(__name__)

# Try to import sensor libraries, use Mock if not available
try:
    import board
    import adafruit_bh1750
    IS_MOCK = False
except (ImportError, NotImplementedError, OSError):
    logger.warning("Adafruit BH1750 libraries not found or hardware not available. Using Mock for BH1750.")
    IS_MOCK = True

def get_lux() -> dict:
    """
    Reads the lux level from the BH1750 sensor.
    Returns a dict with 'lux' value.
    """
    if IS_MOCK or os.environ.get("MOCK_SENSORS") == "true":
        return {
            "lux": 150.0,
            "status": "mock"
        }

    try:
        i2c = board.I2C()
        sensor = adafruit_bh1750.BH1750(i2c)
        lux_val = sensor.lux
        return {
            "lux": round(lux_val, 2),
            "status": "ok"
        }
    except Exception as e:
        logger.error(f"Error reading BH1750 sensor: {e}")
        return {
            "error": str(e),
            "status": "error"
        }
