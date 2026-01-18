
import urllib.request
import urllib.error
import json
import time
import subprocess
import sys
import os

# Configuration
BASE_URL = "http://127.0.0.1:8001"

def start_server():
    print("Starting temporary server on port 8001...")
    python_cmd = "./venv/bin/python" if os.path.exists("./venv/bin/python") else "python3"
    process = subprocess.Popen(
        [python_cmd, "-m", "uvicorn", "main:app", "--port", "8001", "--host", "127.0.0.1"],
        cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(5)
    return process

def post_json(url, data):
    req = urllib.request.Request(
        url, 
        data=json.dumps(data).encode('utf-8'), 
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    try:
        with urllib.request.urlopen(req) as response:
            return response.getcode(), json.load(response)
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8')
    except Exception as e:
        return 0, str(e)

def main():
    server_process = start_server()
    try:
        # Test sending "50" as mode - checking if it sets humidity
        # Note: We need to bypass the Enums/Validation in routes/schemas if we use the strictly typed endpoint.
        # But wait, routes.py uses HumidifierSettings which uses HumidifierMode Enum.
        # "50" is not in HumidifierMode.
        # So I cannot test this via the `control_humidifier_settings` endpoint without modification.
        # I should use the python client directly or modify the schema temporarily?
        # Or I can use the logic from the client directly in this script.
        
        # Actually, let's just use the SwitchBotClient directly in this script to bypass FastAPI validation.
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from app.services.switchbot import SwitchBotClient
        from app.core.config import get_settings
        
        # Load env
        from dotenv import load_dotenv
        load_dotenv()
        
        settings = get_settings()
        humidifier_id = settings.SWITCHBOT_HUMIDIFIER_DEVICE_ID
        client = SwitchBotClient()
        
        print(f"Sending setMode '50' to device {humidifier_id} directly...")
        resp = client.send_command(
            device_id=humidifier_id,
            command="setMode",
            parameter="45", # Try 45%
            command_type="command"
        )
        print(f"Response: {resp}")

    finally:
        print("Stopping server (if started)...")
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    main()
