
import os
import sys
import json
from dotenv import load_dotenv

# Add parent directory to path to import app modules
# Assuming this script is run from sensor-node/scripts or sensor-node/
sys.path.append(os.path.join(os.getcwd()))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.switchbot import SwitchBotClient

def main():
    # Load .env from sensor-node root
    # Adjust path if necessary
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    if os.path.exists(env_path):
        load_dotenv(env_path)
    else:
        print(f"Warning: .env not found at {env_path}")

    client = SwitchBotClient()
    try:
        devices = client.get_devices()
        print(json.dumps(devices, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
