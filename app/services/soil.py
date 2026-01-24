import os
import logging

# Configuration for calibration (based on provided script)
DRY_VAL = 16700  # Air (0%)
WET_VAL = 4300   # Water (100%)
GAIN = 1

logger = logging.getLogger(__name__)

# Try to import Adafruit_ADS1x15, use Mock if not available (e.g., dev environment)
try:
    import Adafruit_ADS1x15
    adc = Adafruit_ADS1x15.ADS1115()
    IS_MOCK = False
except (ImportError, OSError):
    logger.warning("Adafruit_ADS1x15 not found or I2C not available. Using Mock for Soil Sensor.")
    adc = None
    IS_MOCK = True

def get_moisture_percent_from_value(value: int) -> float:
    """Calculates soil moisture percentage from raw ADC value."""
    # Clamp value
    if value > DRY_VAL: value = DRY_VAL
    if value < WET_VAL: value = WET_VAL

    # Linear interpolation: Lower value means wetter
    span = DRY_VAL - WET_VAL
    if span == 0: return 0.0
    percent = 100 * (DRY_VAL - value) / span
    return percent

def get_soil_moisture() -> dict:
    """
    Reads the soil moisture level from the sensor.
    Returns a dict with 'raw_value' and 'moisture_percent'.
    """
    if IS_MOCK or os.environ.get("MOCK_SENSORS") == "true":
        # Return a dummy value for testing
        return {
            "raw_value": 10500,
            "moisture_percent": 50.0,
            "status": "mock"
        }

    try:
        # Read ADC channel 0
        raw_val = adc.read_adc(0, gain=GAIN)
        moisture = get_moisture_percent_from_value(raw_val)
        return {
            "raw_value": raw_val,
            "moisture_percent": round(moisture, 1),
            "status": "ok"
        }
    except Exception as e:
        logger.error(f"Error reading soil sensor: {e}")
        return {
            "error": str(e),
            "status": "error"
        }
