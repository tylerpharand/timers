# Generate GRPC
# python -m grpc_tools.protoc --proto_path=./grpc_src --python_out=./python_out --grpc_python_out=./grpc_python_out v1.proto

from dotenv import load_dotenv
from flask import Flask, jsonify
import json
import os
from assistant_service import AssistantService

load_dotenv()
app = Flask(__name__)

GOOGLE_USERNAME = os.environ.get('GOOGLE_USERNAME')
GOOGLE_PASSWORD = os.environ.get('GOOGLE_PASSWORD')
ASSISTANT_IP = os.environ.get('ASSISTANT_IP')
ASSISTANT_NAME = os.environ.get('ASSISTANT_NAME')

assistant_service = AssistantService(
    assistant_ip=ASSISTANT_IP,
    assistant_name=ASSISTANT_NAME,
    google_username=GOOGLE_USERNAME,
    google_password=GOOGLE_PASSWORD,
)


@app.route('/timers', methods=['GET'])
def timers() -> str:
    timers = assistant_service.get_timers()
    response = jsonify(timers)

    # Enable Access-Control-Allow-Origin
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


app.run()
