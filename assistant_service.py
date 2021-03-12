from google_api_service import GoogleAPIService
import requests
from typing import Optional


class AssistantService:
    google_api_service: GoogleAPIService
    assistant_name: str
    assistant_ip: str
    local_auth_token: Optional[str]

    def __init__(
        self,
        assistant_ip: str,
        assistant_name: str,
        google_username: str,
        google_password: str,
    ):
        self.google_api_service = GoogleAPIService(google_username, google_password)
        self.assistant_name = assistant_name
        self.assistant_ip = assistant_ip
        self.local_auth_token = None

    def local_auth_token_is_expired(self) -> bool:
        if self.local_auth_token is None:
            return True

        return False

    def refresh_local_auth_token(self) -> None:
        devices = self.google_api_service.get_devices()

        # Filter Devices by Google Nest Mini
        google_nest_minis = [device for device in devices if device.device_name == self.assistant_name]
        self.local_auth_token = google_nest_minis[0].local_auth_token

    def get_timers(self) -> list:
        if self.local_auth_token_is_expired():
            self.refresh_local_auth_token()

        # Fetch Alarms and Timers
        res = requests.get(
            url='https://{ip}:8443/setup/assistant/alarms'.format(ip=self.assistant_ip),
            verify=False,
            headers={'cast-local-authorization-token': self.local_auth_token},
        )

        if (res.status_code != 200):
            # TODO: Handle token expiration errors
            raise Exception('Unable to reach Google Nest Mini ({ip})'.format(ip=self.assistant_ip))

        timers = res.json()['timer']

        return timers
