import hashlib
import hmac
import time
import uuid
import base64
import os
import json
import urllib.request
import urllib.error
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
            'nonce': nonce,
            'Content-Type': 'application/json; charset=utf8'
        }

    def _request(self, url: str) -> dict:
        headers = self._get_auth_headers()
        req = urllib.request.Request(url, headers=headers)
        
        try:
            with urllib.request.urlopen(req) as response:
                body = response.read()
                data = json.loads(body)
                
                if data.get("statusCode") != 100:
                    raise HTTPException(
                        status_code=response.getcode(),
                        detail=f"Switchbot API error: {data.get('message')}"
                    )
                return data.get("body", {})
                
        except urllib.error.HTTPError as e:
            detail = e.read().decode('utf-8') if e.fp else str(e)
            raise HTTPException(status_code=e.code, detail=f"Switchbot API HTTP error: {detail}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to communicate with Switchbot API: {str(e)}")

    def get_device_status(self, device_id: str) -> dict:
        url = f"{self.base_url}/devices/{device_id}/status"
        return self._request(url)

    def get_devices(self) -> dict:
        """Fetch the list of all devices."""
        url = f"{self.base_url}/devices"
        return self._request(url)
