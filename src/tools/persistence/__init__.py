import os
import pickle

from typing import Set

from cgg import Node
from controller import Controller


class Persistence:
    output_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'output'))

    @staticmethod
    def dump_cgg(cgg: Node):

        if cgg.session_name is not None:
            output_folder = f"{Persistence.output_folder}/{cgg.session_name}"
        else:
            output_folder = f"{Persistence.output_folder}"

        output_file = f"{output_folder}/cgg.dat"

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        file = open(output_file, 'wb')
        pickle.dump(cgg, file)
        file.close()

    @staticmethod
    def dump_goals(set_goals: Set[Node], subfolder_name: str = None):

        if subfolder_name is not None:
            output_folder = f"{Persistence.output_folder}/{subfolder_name}"
        else:
            output_folder = f"{Persistence.output_folder}"

        output_file = f"{output_folder}/goals.dat"

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        file = open(output_file, 'wb')
        pickle.dump(set_goals, file)
        file.close()

    @staticmethod
    def dump_controller(controller: Controller, folder_path: str, name: str = None):

        if name is None:
            name = "controller"

        output_file = f"{folder_path}/{name}.dat"

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        file = open(output_file, 'wb')
        pickle.dump(controller, file)
        file.close()

    @staticmethod
    def load_cgg(session_folder_name: str) -> Node:

        if session_folder_name is not None:
            output_folder = f"{Persistence.output_folder}/{session_folder_name}"
        else:
            output_folder = f"{Persistence.output_folder}"

        file = f"{output_folder}/cgg.dat"

        file = open(file, 'rb')
        cgg = pickle.load(file)
        file.close()

        return cgg

    @staticmethod
    def load_controller(folder_path: str, name: str = None) -> Controller:

        if name is None:
            file = f"{folder_path}/controller.dat"
        else:
            file = f"{folder_path}/{name}.dat"

        file = open(file, 'rb')
        controller = pickle.load(file)
        file.close()

        return controller

    @staticmethod
    def load_goals(subfolder_name: str = None) -> Set[Node]:

        if subfolder_name is not None:
            output_folder = f"{Persistence.output_folder}/{subfolder_name}"
        else:
            output_folder = f"{Persistence.output_folder}"

        file = f"{output_folder}/goals.dat"

        file = open(file, 'rb')
        set_goals = pickle.load(file)
        file.close()

        return set_goals
