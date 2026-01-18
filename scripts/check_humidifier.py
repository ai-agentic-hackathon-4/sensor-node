
import os
import sys
import json
from dotenv import load_dotenv

# Add app to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.switchbot import SwitchBotClient
from app.core.config import get_settings

def main():
    load_dotenv()
    settings = get_settings()
    humidifier_id = settings.SWITCHBOT_HUMIDIFIER_DEVICE_ID
    
    if not humidifier_id:
        print("Humidifier ID not set in config.")
        return

    client = SwitchBotClient()
    
    print(f"Checking Humidifier ID: {humidifier_id}")
    
    try:
        # Get Device List to find type
        devices = client.get_devices()
        device_lists = devices.get("deviceList", []) + devices.get("infraredRemoteList", [])
        
        target_device = next((d for d in device_lists if d["deviceId"] == humidifier_id), None)
        
        if target_device:
            print("Device Info:")
            print(json.dumps(target_device, indent=2, ensure_ascii=False))
        else:
            print("Device not found in list.")

        # Get Status
        status = client.get_device_status(humidifier_id)
        print("\nDevice Status:")
        print(json.dumps(status, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
