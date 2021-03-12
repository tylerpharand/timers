from token_dispenser import TokenDispenser
import grpc
from v1_pb2 import GetHomeGraphRequest
from v1_pb2_grpc import StructuresServiceStub


class GoogleAPIService:
    def __init__(self, username: str, password: str):
        self.token_dispener = TokenDispenser(username, password)

    def get_devices(self) -> list:
        # Get Access Token
        token = self.token_dispener.dispense()

        # Get Devices on Network
        creds = grpc.access_token_call_credentials(token)
        ssl = grpc.ssl_channel_credentials()
        composite = grpc.composite_channel_credentials(ssl, creds)
        channel = grpc.secure_channel('googlehomefoyer-pa.googleapis.com:443', composite)
        service = StructuresServiceStub(channel)
        grpc_res = service.GetHomeGraph(GetHomeGraphRequest())

        return grpc_res.home.devices
