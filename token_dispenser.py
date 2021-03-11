from uuid import getnode as getmac
from gpsoauth import perform_master_login, perform_oauth


class TokenDispenser:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    @staticmethod
    def _get_android_id() -> str:
        mac_int = getmac()
        android_id = TokenDispenser._create_mac_string(mac_int)
        android_id = android_id.replace(':', '')

        return android_id

    @staticmethod
    def _create_mac_string(num: int, splitter: str = ':') -> str:
        mac = hex(num)[2:]
        if mac[-1] == 'L':
            mac = mac[:-1]
        pad = max(12 - len(mac), 0)
        mac = '0' * pad + mac
        mac = splitter.join([mac[x:x + 2] for x in range(0, 12, 2)])
        mac = mac.upper()

        return mac

    def _get_master_token(self, android_id: str) -> str:
        res = perform_master_login(self.username, self.password, android_id)
        if 'Token' not in res:
            raise Exception('Unable to fetch master token')

        return res['Token']

    def _get_access_token(self, master_token: str, android_id: str) -> str:
        res = perform_oauth(
            self.username, master_token, android_id,
            app='com.google.android.apps.chromecast.app',
            service='oauth2:https://www.google.com/accounts/OAuthLogin',
            client_sig='24bb24c05e47e0aefa68a58a766179d9b613a600'
        )

        if 'Auth' not in res:
            raise Exception('Unable to fetch access token')

        return res['Auth']

    def dispense(self) -> str:
        device_id = self._get_android_id()
        master_token = self._get_master_token(device_id)
        access_token = self._get_access_token(master_token, device_id)

        return access_token
