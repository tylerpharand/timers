from dotenv import load_dotenv
from token_dispenser import TokenDispenser
import os
import requests
import grpc
from v1_pb2 import GetHomeGraphRequest
from v1_pb2_grpc import StructuresServiceStub

load_dotenv()

# Generate GRPC
# python -m grpc_tools.protoc --proto_path=./grpc_src --python_out=./python_out --grpc_python_out=./grpc_python_out v1.proto


def main() -> None:
    # TODO: Automatically get IP Address
    ip = '192.168.0.11'
    username = os.environ.get('GOOGLE_USERNAME')
    password = os.environ.get('GOOGLE_PASSWORD')

    # Get Access Token
    token_dispener = TokenDispenser(username, password)
    token = token_dispener.dispense()

    # Get Devices on Network
    creds = grpc.access_token_call_credentials(token)
    ssl = grpc.ssl_channel_credentials()
    composite = grpc.composite_channel_credentials(ssl, creds)
    channel = grpc.secure_channel('googlehomefoyer-pa.googleapis.com:443', composite)
    service = StructuresServiceStub(channel)
    grpc_res = service.GetHomeGraph(GetHomeGraphRequest())
    devices = grpc_res.home.devices

    # Filter Devices by Google Nest Mini
    google_nest_minis = [device for device in devices if device.hardware.model == 'Google Nest Mini']
    local_auth_token = google_nest_minis[0].local_auth_token

    # Fetch Alarms and Timers
    res = requests.get(
        url='https://{ip}:8443/setup/assistant/alarms'.format(ip=ip),
        verify=False,
        headers={'cast-local-authorization-token': local_auth_token},
    )

    if (res.status_code != 200):
        raise Exception('Unable to reach Google Nest Mini ({ip})'.format(ip=ip))

    timers = res.json()['timer']

    print(timers)


main()
