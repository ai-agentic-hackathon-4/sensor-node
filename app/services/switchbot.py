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

from app.schemas.switchbot import ACSettings, HumidifierSettings, SwitchBotCommand, PlugMiniSettings

from app.core.config import get_settings

class SwitchBotClient:
    def __init__(self):
        self.settings = get_settings()
        self.token = self.settings.SWITCHBOT_TOKEN
        self.secret = self.settings.SWITCHBOT_SECRET
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

    def _request(self, url: str, method: str = "GET", body_data: dict = None) -> dict:
        headers = self._get_auth_headers()
        
        data = None
        if body_data:
            data = json.dumps(body_data).encode('utf-8')
            
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        
        try:
            with urllib.request.urlopen(req) as response:
                body = response.read()
                # For some commands, body might be empty or just status
                if not body:
                    return {}
                try:
                    data = json.loads(body)
                except json.JSONDecodeError:
                     return {}
                
                if data.get("statusCode") != 100:
                    pass
                    
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

    def send_command(self, device_id: str, command: str, parameter: str = "default", command_type: str = "command") -> dict:
        """Send a command to a device."""
        url = f"{self.base_url}/devices/{device_id}/commands"
        body = {
            "command": command,
            "parameter": parameter,
            "commandType": command_type
        }
        return self._request(url, method="POST", body_data=body)

    def control_ac_settings(self, settings: ACSettings, device_id: str) -> dict:
        # Format parameter: temp, mode, fan, power
        power_str = "on" if settings.is_on else "off"
        parameter = f"{settings.temperature},{settings.mode.value},{settings.fan_speed.value},{power_str}"
        
        return self.send_command(
            device_id=device_id,
            command="setAll",
            parameter=parameter,
            command_type="command"
        )

    def control_humidifier_settings(self, settings: HumidifierSettings, device_id: str) -> dict:
        if not settings.is_on:
            return self.send_command(
                device_id=device_id,
                command="turnOff",
                command_type="command"
            )
        
        # Ensure ON
        self.send_command(device_id=device_id, command="turnOn")
        
        time.sleep(1)
        
        # Humidifier 2 requires a JSON object parameter (passed as dict)
        # Default target humidity to 50% if not specified
        parameter = {
            "mode": int(settings.mode.value),
            "targetHumidify": 50
        }
        
        return self.send_command(
            device_id=device_id,
            command="setMode",
            parameter=parameter,
            command_type="command"
        )

    def control_plug_mini(self, settings: PlugMiniSettings, device_id: str) -> dict:
        if not settings.is_on:
            return self.send_command(
                device_id=device_id,
                command="turnOff",
                command_type="command"
            )

        return self.send_command(
            device_id=device_id,
            command="turnOn",
            command_type="command"
        )

