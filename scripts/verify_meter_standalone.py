import os
import json
import time
import uuid
import base64
import hmac
import hashlib
import urllib.request
import urllib.error
import sys

def load_env_manual():
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    if os.path.exists(env_path):
        print(f"Loading .env from {env_path}")
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'): continue
                if '=' in line:
                    key, val = line.split('=', 1)
                    if key.strip():
                        val = val.strip()
                        # Remove quotes
                        if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                            val = val[1:-1]
                        os.environ[key.strip()] = val
    else:
        print(f"Warning: .env file not found at {env_path}")

def get_auth_header(token, secret):
    nonce = str(uuid.uuid4())
    t = str(int(round(time.time() * 1000)))
    string_to_sign = '{}{}{}'.format(token, t, nonce)
    
    string_to_sign = bytes(string_to_sign, 'utf-8')
    secret = bytes(secret, 'utf-8')
    
    sign = base64.b64encode(hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())
    
    return {
        'Authorization': token,
        't': t,
        'sign': str(sign, 'utf-8'),
        'nonce': nonce,
        'Content-Type': 'application/json; charset=utf8'
    }

def main():
    load_env_manual()
    token = os.environ.get("SWITCHBOT_TOKEN")
    secret = os.environ.get("SWITCHBOT_SECRET")
    device_id = os.environ.get("SWITCHBOT_METER_DEVICE_ID")
    
    if not token or not secret:
        print("Error: SWITCHBOT_TOKEN and SWITCHBOT_SECRET must be set in .env")
        return
    
    if not device_id:
        print("Error: SWITCHBOT_METER_DEVICE_ID must be set in .env")
        # Try to find a default if not set, just to be helpful? No, strict check first.
        return

    print(f"Verifying Switchbot API for Device ID: {device_id}")

    url = f"https://api.switch-bot.com/v1.1/devices/{device_id}/status"
    headers = get_auth_header(token, secret)
    
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            body = response.read()
            data = json.loads(body)
            
            status_code = data.get("statusCode")
            if status_code != 100:
                print(f"API Error: {data.get('message')}")
                return

            device_status = data.get("body", {})
            print("Successfully fetched device status:")
            print(json.dumps(device_status, indent=2, ensure_ascii=False))
            
            temp = device_status.get("temperature")
            humidity = device_status.get("humidity")
            
            if temp is not None and humidity is not None:
                print(f"\n[OK] Temperature: {temp}°C")
                print(f"[OK] Humidity: {humidity}%")
            else:
                print("\n[WARNING] Temperature or Humidity not found in response.")

    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} {e.reason}")
        print(e.read().decode('utf-8'))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
