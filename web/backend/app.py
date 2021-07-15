import os
import shutil
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
                            default_project.append({"title": os.path.splitext(file)[0], "content": json_str})
                list_of_projects.append(default_project)

    emit("receive-projects", list_of_projects)


@socketio.on('save-project')
def save_project(data):
    print("SAVE PROJECT")
    print(data)
    session_dir = os.path.join(storage_folder, f"sessions/{data['world']['info']['session_id']}")
    if not os.path.isdir(session_dir):
        os.mkdir(session_dir)
    project_dir = os.path.join(session_dir, f"{data['world']['info']['project_id']}")
    if not os.path.isdir(project_dir):
        os.mkdir(project_dir)
    goals_dir = os.path.join(project_dir, "goals")
    if not os.path.isdir(goals_dir):
        os.mkdir(goals_dir)
    list_of_files = ["environment", "info"]
    for filename in list_of_files:
        json_file = open(os.path.join(project_dir, filename + ".json"), "w")
        json_formatted = json.dumps(data['world'][filename], indent=4, sort_keys=True)
        json_file.write(json_formatted)
        json_file.close()


@socketio.on('save-goals')
def save_goals(data):
    print("SAVE GOALS")
    print(data)
    goals_dir = os.path.join(storage_folder, f"sessions/{data['session']}/{data['projectId']}/goals")
    for i in range(len(data['goals'])) :
        j = i
        file = str(j) + ".json"
        while os.path.isfile(os.path.join(goals_dir, file)):
            j += 1
            file = str(j) + ".json"

        json_file = open(os.path.join(goals_dir, file), "w")
        json_formatted = json.dumps(data['goals'][j], indent=4, sort_keys=True)
        json_file.write(json_formatted)
        json_file.close()


@socketio.on('delete-project')
def delete_project(data):
    current_session_folder = Path(os.path.join(storage_folder, f"sessions/{data['session']}"))
    dir_path, dir_names, filenames = next(walk(current_session_folder))
    i = 1
    for name in dir_names:
        if i == data['index']:
            if len(dir_names) == 1:
                shutil.rmtree(current_session_folder)
            else:
                dir_to_delete = Path(os.path.join(current_session_folder, name))
                shutil.rmtree(dir_to_delete)
        i += 1


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
