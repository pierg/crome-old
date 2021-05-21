from os import path

import time
from flask import Flask, request, Blueprint, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit

if path.exists('../frontend/build'):
    app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')
else:
    app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'

# Set this variable to None, "threading", "eventlet" or "gevent"
socketio = SocketIO(app, async_mode=None)


CORS(app)
api = Blueprint('api', __name__)
app.register_blueprint(api, url_prefix='/api')


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



@app.route('/')
def index():
    return app.send_static_file('index.html')


@api.route('/submit', methods=['POST'])
def handle_submit():
    if request.method == "POST":
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        job = request.form['job']
        print(f'first name : {first_name}')
        print(f'last name : {last_name}')
        print(f'job : {job}')

        # do your processing logic here.

        return jsonify({
            "firstName": first_name,
            "lastName": last_name,
            "job": job
        })


@app.route('/time')
def get_current_time():
    return {'time': time.time()}




if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
