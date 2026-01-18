from fastapi.testclient import TestClient
from app.api.routes import router
from fastapi import FastAPI
import os

# Create a minimal app for testing the router
app = FastAPI()
app.include_router(router)

client = TestClient(app)

def test_soil_endpoint():
    print("Testing /sensor/soil endpoint...")
    
    # Force MOCK_SENSORS to true to ensure mock path is tested even if I2C connects by chance
    os.environ["MOCK_SENSORS"] = "true"
    
    try:
        response = client.get("/sensor/soil")
        
        print(f"Status Code: {response.status_code}")
        print(f"Response JSON: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            if "moisture_percent" in data:
                print("✅ Verification SUCCESS: Endpoint returned moisture data.")
            else:
                print("❌ Verification FAILED: Response missing 'moisture_percent'.")
        else:
            print("❌ Verification FAILED: Non-200 status code.")
            
    except Exception as e:
        print(f"❌ Verification FAILED with error: {e}")

if __name__ == "__main__":
    test_soil_endpoint()
