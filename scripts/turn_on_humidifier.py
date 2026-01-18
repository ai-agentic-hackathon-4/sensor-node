
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
    # Use venv python if available
    python_cmd = "./venv/bin/python" if os.path.exists("./venv/bin/python") else "python3"
    
    process = subprocess.Popen(
        [python_cmd, "-m", "uvicorn", "main:app", "--port", "8001", "--host", "127.0.0.1"],
        cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(5) # Wait for startup
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
        print("Turning ON Humidifier...")
        status, resp = post_json(f"{BASE_URL}/control/humidifier", {"command": "turnOn"})
        print(f"Status: {status}")
        print(f"Response: {resp}")
    finally:
        print("Stopping server...")
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    main()
