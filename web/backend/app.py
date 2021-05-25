import os
from os import path

import time
from pathlib import Path

from flask import Flask, request
from flask_socketio import SocketIO, emit
import json

if path.exists('../frontend/build'):
    app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')
else:
    app = Flask(__name__)

storage_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'storage'))

# socketio = SocketIO(app, cors_allowed_origins="*")
socketio = SocketIO(app, cors_allowed_origins='http://localhost:3000')


@socketio.on('get-patterns')
def get_patterns():
    print('Get patterns')
    print(request.args)
    print(f'ID {request.args.get("id")}')

    robotic_patterns_file = Path(os.path.join(storage_folder, 'crome/patterns/robotic.json'))
    with open(robotic_patterns_file) as json_file:
        robotic_patterns = json.load(json_file)

    emit("receive-patterns", {'robotic': json.dumps(robotic_patterns)})


@socketio.on('connect')
def connected():
    print('Connected')
    print(request.args)
    print(f'ID {request.args.get("id")}')


@socketio.on('disconnect')
def disconnected():
    print('Disconnected')
    print(request.args)
    print(f'ID {request.args.get("id")}')


@socketio.on('get-message')
def get_message_test():
    print('GET ENVIRONMENTS')
    print(request.args)
    print(f'ID {request.args.get("id")}')
    emit("receive-message", {'data': "Message from Server"})
    time.sleep(3)
    emit("receive-message", {'data': "Message after 3 seconds from the first"})


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/time')
def get_current_time():
    return {'time': time.time()}


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
