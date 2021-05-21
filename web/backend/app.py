from os import path

import time
from flask import Flask, request
from flask_socketio import SocketIO, emit

if path.exists('../frontend/build'):
    app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')
else:
    app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'

# Set this variable to None, "threading", "eventlet" or "gevent"
socketio = SocketIO(app, async_mode=None)


@socketio.on('get-environments')
def on_connect():
    print('-----------------------')
    print('Client connected - %s' + request.sid)
    print('-----------------------')
    emit('receive-environments',
         {'type': "success", 'content': "New goal created"})


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/time')
def get_current_time():
    return {'time': time.time()}


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
