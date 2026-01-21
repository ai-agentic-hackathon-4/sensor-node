
import asyncio
import httpx

async def main():
    url = "http://192.168.11.226:8000/control/air-conditioner/settings"
    payload = {
        "temperature": 25,
        "mode": 5,
        "fan_speed": 1,
        "is_on": True
    }
    print(f"Testing POST to {url} with {payload}")
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(url, json=payload)
            print(f"Status: {resp.status_code}")
            print(f"Response: {resp.text}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
