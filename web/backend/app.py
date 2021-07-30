import os
import shutil
from os import walk

import time
from pathlib import Path

import base64

from flask import Flask, request
from flask_socketio import SocketIO, emit
import json

import threading
from time import strftime

backend_folder = Path(__file__).parent.absolute()
print(backend_folder)

front_end_folder = Path(__file__).parents[1].absolute() / 'frontend'
build_folder = front_end_folder / 'build'
print(build_folder)
storage_folder = Path(__file__).parents[1].absolute() / 'storage'
print(storage_folder)


if build_folder.exists():
    app = Flask(__name__, static_folder=str(build_folder), static_url_path='/')
else:
    app = Flask(__name__)

socketio = SocketIO(app, cors_allowed_origins='*')

users = {}


@socketio.on('connect')
def connected():
    print('Connected')
    print(request.args)
    print(f'ID {request.args.get("id")}')
    lock = threading.Lock()
    lock.acquire()
    users[request.args.get("id")] = request.sid
    now = time.localtime(time.time())
    emit("send-message", strftime("%H:%M:%S", now) + " Connected", room=request.sid)
    lock.release()


@socketio.on('get-projects')
def get_projects(data):
    list_of_projects = []  # array that will be sent containing all projects #

    list_of_sessions = [f"sessions/default", f"sessions/{data['session']}"]

    for sessions in list_of_sessions:
        session_folder = storage_folder / sessions
        if os.path.isdir(session_folder):  # if there is a folder for this session #
            dir_path, dir_names, filenames = next(walk(session_folder))
            for subdir in dir_names:
                project_folder = Path(os.path.join(dir_path, subdir))
                project_path, project_directories, project_files = next(walk(project_folder))
                default_project = []
                for file in project_files:
                    if os.path.splitext(file)[1] == ".json":
                        with open(Path(os.path.join(project_path, file))) as json_file:
                            json_obj = json.load(json_file)
                            json_str = json.dumps(json_obj)
                            default_project.append({"title": os.path.splitext(file)[0], "content": json_str})
                    if os.path.splitext(file)[1] == ".png":
                        with open(Path(os.path.join(project_path, file)), "rb") as png_file:
                            read_png_file = base64.b64encode(png_file.read())
                            default_project.append({"title": "image", "content": read_png_file})

                list_of_projects.append(default_project)

    emit("receive-projects", list_of_projects, room=request.sid)


@socketio.on('save-project')
def save_project(data):
    print("SAVE PROJECT : "+str(data['session']))
    session_id = data['world']['info']['session_id']
    session_dir = os.path.join(storage_folder, f"sessions/{session_id}")
    if not os.path.isdir(session_dir):
        os.mkdir(session_dir)
    is_simple = data['world']['info']['project_id'] == "simple"
    if is_simple:
        number_of_copies = 1
        while os.path.isdir(os.path.join(storage_folder, f"sessions/{session_id}/simple_{number_of_copies}")):
            number_of_copies += 1
        data['world']['environment']['project_id'] = f"simple_{number_of_copies}"
        data['world']['info']['project_id'] = f"simple_{number_of_copies}"
    project_dir = os.path.join(session_dir, f"{data['world']['info']['project_id']}")
    if not os.path.isdir(project_dir):
        os.mkdir(project_dir)
    goals_dir = os.path.join(project_dir, "goals")
    if not os.path.isdir(goals_dir):
        if is_simple:
            shutil.copytree(os.path.join(storage_folder, "sessions/default/simple/goals"), goals_dir)
        else:
            os.mkdir(goals_dir)
    list_of_files = ["environment", "info"]
    for filename in list_of_files:
        json_file = open(os.path.join(project_dir, filename + ".json"), "w")
        json_formatted = json.dumps(data['world'][filename], indent=4, sort_keys=True)
        json_file.write(json_formatted)
        json_file.close()
    name = data['world']['info']['name']
    now = time.localtime(time.time())
    emit("send-message", strftime("%H:%M:%S", now) + " The project \"" + name + "\" has been saved.",
         room=users[session_id])


@socketio.on('save-image')
def save_image(data):
    img_data = (bytes(data["image"], 'utf-8'))

    current_project_image = Path(
        os.path.join(storage_folder, f"sessions/{data['session']}/{data['project']}/environment.png"))

    with open(current_project_image, "wb") as fh:
        fh.write(base64.decodebytes(img_data))


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
    emit("deletion-complete", True, room=request.sid)
    now = time.localtime(time.time())
    emit("send-message", strftime("%H:%M:%S", now) + " The project has been deleted.",
         room=users[data['session']])


@socketio.on('get-goals')
def get_goals(data):
    goals_folder = Path(os.path.join(storage_folder, f"sessions/{data['session']}/{data['project']}/goals"))

    """Retrieving files"""
    if os.path.isdir(goals_folder):
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

        emit("receive-goals", list_of_goals, room=request.sid)


@socketio.on('add-goal')
def add_goal(data):
    project_id = data['projectId']
    is_simple = str(project_id) == "simple"
    if is_simple:
        number_of_copies = 1
        while os.path.isdir(os.path.join(storage_folder, f"sessions/{data['session']}/simple_{number_of_copies}")):
            number_of_copies += 1
        project_id = f"simple_{number_of_copies}"
        shutil.copytree(os.path.join(storage_folder, "sessions/default/simple"),
                        os.path.join(storage_folder,  f"sessions/{data['session']}/{project_id}"))
        list_save = ["info", "environment"]
        for i in list_save:
            with open(os.path.join(storage_folder, f"sessions/{data['session']}/{project_id}/{i}.json"), "r") as file:
                json_data = json.load(file)
            if i == "info":
                json_data["name"] = f"Simple Gridworld ({number_of_copies})"
            json_data["project_id"] = project_id
            json_data["session_id"] = data['session']
            with open(os.path.join(storage_folder, f"sessions/{data['session']}/{project_id}/info.json"), "w") as file:
                json_formatted = json.dumps(json_data, indent=4, sort_keys=True)
                file.write(json_formatted)

    goals_dir = os.path.join(storage_folder, f"sessions/{data['session']}/{project_id}/goals")
    dir_path, dir_names, filenames = next(walk(goals_dir))
    greatest_id = -1 if len(filenames) == 0 else max(filenames)[0:4]
    greatest_id = int(greatest_id) + 1
    if 'id' not in data['goal']:
        data['goal']['id'] = greatest_id
        greatest_id += 1
    filename = str(data['goal']['id']).zfill(4) + ".json"
    json_file = open(os.path.join(goals_dir, filename), "w")
    json_formatted = json.dumps(data['goal'], indent=4, sort_keys=True)
    json_file.write(json_formatted)
    json_file.close()
    if is_simple:
        emit("saving-simple", project_id, room=request.sid)
    else:
        emit("saving-complete", True, room=request.sid)

    now = time.localtime(time.time())
    name = data['goal']['name']
    emit("send-message", strftime("%H:%M:%S", now) + " The goal \"" + name + "\" has been saved.",
         room=users[data['session']])


@socketio.on('delete-goal')
def delete_goal(data):
    current_goals_folder = Path(os.path.join(storage_folder, f"sessions/{data['session']}/{data['project']}/goals"))
    dir_path, dir_names, filenames = next(walk(current_goals_folder))
    i = 0
    for goal_file in filenames:
        if i == data['index']:
            goal_to_delete = Path(os.path.join(current_goals_folder, goal_file))
            os.remove(goal_to_delete)
        i += 1

    now = time.localtime(time.time())
    emit("send-message", strftime("%H:%M:%S", now) + " The goal has been deleted.", room=users[data['session']])


@socketio.on('get-patterns')
def get_patterns():
    print('Get patterns')
    print(request.args)
    print(f'ID {request.args.get("id")}')

    robotic_patterns_file = Path(os.path.join(storage_folder, 'crome/patterns/robotic.json'))
    with open(robotic_patterns_file) as json_file:
        robotic_patterns = json.load(json_file)

    emit("receive-patterns", {'robotic': json.dumps(robotic_patterns)}, room=request.sid)


@socketio.on('process-goals')
def process_goals(session_id):
    print("BEGIN SLEEP")
    time.sleep(15)
    print("STOP SLEEP")


@socketio.on('process-cgg')
def process_cgg(session_id):
    print("BEGIN SLEEP")
    time.sleep(6)
    print("STOP SLEEP")


@socketio.on('session-existing')
def check_if_session_exist(session_id):
    print("check if following session exists : "+str(session_id))
    sessions_folder = Path(os.path.join(storage_folder, "sessions"))
    dir_path, dir_names, filenames = next(walk(sessions_folder))
    found = False
    for dir_name in dir_names:
        if dir_name == session_id and dir_name != "default":
            found = True
    emit("receive-answer", found, room=request.sid)


@socketio.on('disconnect')
def disconnected():
    print('Disconnected')
    print(request.args)
    print(f'ID {request.args.get("id")}')


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/time')
def get_current_time():
    return {'time': time.time()}


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=3030)
