import sys
import os
import logging
from unittest.mock import MagicMock

# Add the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock fastapi if not installed, as we just want to test the urllib logic in SwitchBotClient
try:
    import fastapi
except ImportError:
    print("FastAPI not installed, mocking for verification...")
    sys.modules["fastapi"] = MagicMock()
    sys.modules["fastapi"].HTTPException = Exception

# Now import the client
from app.services.switchbot import SwitchBotClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_env_manual():
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'): continue
                if '=' in line:
                    key, val = line.split('=', 1)
                    if key.strip():
                        val = val.strip()
                        if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                            val = val[1:-1]
                        os.environ[key.strip()] = val

def verify_client():
    load_env_manual()
    
    token = os.environ.get("SWITCHBOT_TOKEN")
    secret = os.environ.get("SWITCHBOT_SECRET")
    
    if not token or not secret:
        logger.error("Error: SWITCHBOT_TOKEN and SWITCHBOT_SECRET must be set.")
        return

    client = SwitchBotClient()
    device_id = os.environ.get("SWITCHBOT_METER_DEVICE_ID")
    
    if not device_id:
        logger.error("Error: SWITCHBOT_METER_DEVICE_ID must be set.")
        return

    try:
        logger.info(f"Fetching status for device ID: {device_id} using urllib...")
        status = client.get_device_status(device_id)
        logger.info("Successfully fetched device status:")
        logger.info(status)
        
        if "temperature" in status and "humidity" in status:
             logger.info("Verification PASSED.")
        else:
             logger.warning("Verification WARNING: Temperature or Humidity missing in response.")
             
    except Exception as e:
        logger.error(f"Verification FAILED: {e}")

if __name__ == "__main__":
    verify_client()
