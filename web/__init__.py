from flask import Flask, request
from flask_socketio import SocketIO, emit

# Set this type to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None
app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)


@socketio.on('connect')
def on_connect():
    print('-----------------------')
    print('Client connected - %s' + request.sid)
    print('-----------------------')


@socketio.on('disconnect')
def on_disconnect():
    print('-----------------------')
    print('Client disconnect - %s' + request.sid)
    print('-----------------------')



from web import views, models, requests
