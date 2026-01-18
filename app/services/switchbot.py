import hashlib
import hmac
import time
import uuid
import base64
import os
import requests
from fastapi import HTTPException

class SwitchBotClient:
    def __init__(self):
        self.token = os.environ.get("SWITCHBOT_TOKEN")
        self.secret = os.environ.get("SWITCHBOT_SECRET")
        self.base_url = "https://api.switch-bot.com/v1.1"

    def _get_auth_headers(self) -> dict:
        if not self.token or not self.secret:
            raise HTTPException(
                status_code=500, 
                detail="Switchbot credentials not found. Please set SWITCHBOT_TOKEN and SWITCHBOT_SECRET."
            )

        nonce = str(uuid.uuid4())
        t = str(int(round(time.time() * 1000)))
        string_to_sign = '{}{}{}'.format(self.token, t, nonce)

        string_to_sign = bytes(string_to_sign, 'utf-8')
        secret = bytes(self.secret, 'utf-8')

        sign = base64.b64encode(hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())

        return {
            'Authorization': self.token,
            't': t,
            'sign': str(sign, 'utf-8'),
            'nonce': nonce
        }

    def get_device_status(self, device_id: str) -> dict:
        url = f"{self.base_url}/devices/{device_id}/status"
        headers = self._get_auth_headers()
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            if data.get("statusCode") != 100:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Switchbot API error: {data.get('message')}"
                )
                
            return data.get("body", {})
            
        except requests.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch device status: {str(e)}")

    def get_devices(self) -> dict:
        """Fetch the list of all devices."""
        url = f"{self.base_url}/devices"
        headers = self._get_auth_headers()
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            if data.get("statusCode") != 100:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Switchbot API error: {data.get('message')}"
                )
                
            return data.get("body", {})
            
        except requests.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch devices: {str(e)}")
