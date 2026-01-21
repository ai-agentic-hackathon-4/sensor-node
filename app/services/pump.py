import time
import logging
import os

logger = logging.getLogger(__name__)

# Config
PUMP_PIN = 17
FLOW_RATE_PER_SEC = 170.0 / 3.0  # ~56.67 ml/sec

# Mock check
IS_MOCK = False
try:
    import RPi.GPIO as GPIO
except (ImportError, RuntimeError):
    logger.warning("RPi.GPIO not found. Using Mock for Pump Service.")
    IS_MOCK = True
    # create a dummy GPIO class if needed, or just guard in functions

def pour_water(target_ml: float) -> dict:
    """
    Activates the pump to dispense the target volume of water.
    Returns result dict.
    """
    if target_ml <= 0:
        return {"status": "error", "message": "Volume must be positive"}

    duration = target_ml / FLOW_RATE_PER_SEC

    # Check for Mock environment
    if IS_MOCK or os.environ.get("MOCK_SENSORS") == "true":
        logger.info(f"[MOCK] Pouring {target_ml}ml (Duration: {duration:.2f}s)")
        time.sleep(1) # Simulate some delay but not full duration for dev speed? Or full?
        # Let's simulate a short delay for UX
        return {
            "status": "success", 
            "message": f"[MOCK] Poured {target_ml}ml",
            "duration_sec": round(duration, 2)
        }

    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PUMP_PIN, GPIO.OUT)
        
        # Pump ON (LOW)
        logger.info(f"Pump ON for {duration:.2f}s")
        GPIO.output(PUMP_PIN, GPIO.LOW)
        
        time.sleep(duration)
        
        # Pump OFF (HIGH)
        GPIO.output(PUMP_PIN, GPIO.HIGH)
        logger.info("Pump OFF")
        
        return {
            "status": "success",
            "message": f"Poured {target_ml}ml",
            "duration_sec": round(duration, 2)
        }
    except Exception as e:
        logger.error(f"Error controlling pump: {e}")
        # Emergency stop attempt
        try:
            GPIO.output(PUMP_PIN, GPIO.HIGH)
        except:
            pass
        return {"status": "error", "message": str(e)}
    finally:
        if not IS_MOCK:
            GPIO.cleanup()
