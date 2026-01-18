import os
import sys
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch

# Add the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app

client = TestClient(app)

def verify_endpoint_mocked():
    """Verify the endpoint with a mocked SwitchBotClient."""
    print("Verifying endpoint with MOCKED data...")
    device_id = "test_device_id"
    
    mock_status = {
        "temperature": 25.5,
        "humidity": 50,
        "deviceType": "Meter",
        "hubDeviceId": "hub_id",
        "statusCode": 100
    }
    
    with patch("app.api.routes.SwitchBotClient") as MockClient:
        instance = MockClient.return_value
        instance.get_device_status.return_value = mock_status
        
        # Mocking os.environ.get to return a fake device ID for the endpoint logic
        original_environ_get = os.environ.get
        def mock_environ_get(key, default=None):
            if key == "SWITCHBOT_METER_DEVICE_ID":
                return "test_device_id"
            return original_environ_get(key, default)

        with patch("os.environ.get", side_effect=mock_environ_get):
            response = client.get("/sensor/meter") # Updated endpoint
        
            print(f"Status Code: {response.status_code}")
            print(f"Response Body: {response.json()}")
            
            assert response.status_code == 200
            data = response.json()
            assert data["temperature"] == 25.5
            assert data["humidity"] == 50
            # Simplified response, metadata removed
            assert "deviceId" not in data

        
    print("Mock Verification PASSED.")

if __name__ == "__main__":
    verify_endpoint_mocked()
