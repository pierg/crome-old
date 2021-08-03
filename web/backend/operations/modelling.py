import json
import os
from os import walk
from pathlib import Path

from tools.persistence import Persistence
from world import World


class Modelling:

    @staticmethod
    def create_environment(project_folder):

        # dir_path, dir_names, filenames = next(walk(project_folder))
        with open(Path(os.path.join(project_folder, "environment.json"))) as json_file:
            json_obj = json.load(json_file)

        w = World(project_name=json_obj["project_id"])
        for action in json_obj["actions"]:
            w.new_boolean_action(action["name"])
        for location in json_obj["grid"]["locations"]:
            w.new_boolean_location(location["id"], mutex="locations", adjacency=location["adjacency"])
        w.new_boolean_context("day", mutex="time")
        w.new_boolean_context("night", mutex="time")

        # TODO: save the world instance in the project_folder
        Persistence.dump_world(w, project_folder)
