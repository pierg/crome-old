import os
from os import path, walk

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

'''
@socketio.on('get-projects')
def get_projects(data):
    print(data)
    print('Getting Projects')
    print(request.args)
    print(f'ID {request.args.get("id")}')
    print(f'Session {request.args.get("session")}')
    print(f'Project {request.args.get("simple")}')

    session_folder = Path(os.path.join(storage_folder, f"sessions/{data['session']}"))

    """Retrieving files"""
    files_paths = []
    dirpath, dirnames, filenames = next(walk(session_folder))
    for dir in dirnames:
        print(dir)
    for file in filenames:
        files_paths.append(Path(os.path.join(dirpath, file)))

    list_of_projects = []
    for file in files_paths:
        with open(file) as json_file:
            json_obj = json.load(json_file)
            json_str = json.dumps(json_obj)
            list_of_projects.append(json_str)

    emit("receive-projects", list_of_projects)


'''


@socketio.on('get-projects')
def get_projects(data):
    list_of_projects = []  # array that will be sent containing all projects #

    list_of_sessions = [f"sessions/default", f"sessions/{data['session']}"]

    for sessions in list_of_sessions:
        session_folder = Path(os.path.join(storage_folder, sessions))
        if os.path.isdir(session_folder):  # if there is a folder for this session #
            dir_path, dir_names, filenames = next(walk(session_folder))
            for subdir in dir_names:
                project_folder = Path(os.path.join(dir_path, subdir))
                project_path, project_directories, project_files = next(walk(project_folder))
                default_project = []
                for file in project_files:
                    with open(Path(os.path.join(project_path, file))) as json_file:
                        if os.path.splitext(file)[1] == ".json":
                            json_obj = json.load(json_file)
                            json_str = json.dumps(json_obj)
                            default_project.append(json_str)
                list_of_projects.append(default_project)

    emit("receive-projects", list_of_projects)


@socketio.on('save-project')
def save_project(data):
    print("SAVE PROJECT")
    print(data)


@socketio.on('get-goals')
def get_goals(data):
    # print(data)
    # print('Getting Goals')
    # print(request.args)
    # print(f'ID {request.args.get("id")}')
    # print(f'Session {request.args.get("session")}')
    # print(f'Project {request.args.get("project")}')

    goals_folder = Path(os.path.join(storage_folder, f"sessions/{data['session']}/{data['project']}/goals"))

    """Retrieving files"""
    files_paths = []
    dirpath, dirnames, filenames = next(walk(goals_folder))
    for file in filenames:
        files_paths.append(Path(os.path.join(dirpath, file)))

    list_of_goals = []
    for file in files_paths:
        with open(file) as json_file:
            json_obj = json.load(json_file)
            json_str = json.dumps(json_obj)
            list_of_goals.append(json_str)

    emit("receive-goals", list_of_goals)


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


@socketio.on('get-gridworld')
def send_gridwolrd():
    gridworld_file = Path(os.path.join(storage_folder, 'sessions/default/simple/environment.json'))
    with open(gridworld_file) as json_file:
        gridworld = json.load(json_file)
    emit("receive-gridwolrd", json.dumps(gridworld))


@socketio.on('test')
def test():
    i = 0
    while True:
        emit("receive-message", i)
        i += 1
        time.sleep(3)


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
    app.run(host='127.0.0.1', debug=True, port=5000)
