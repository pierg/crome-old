import os
from pathlib import Path
from typing import Set

import dill as dill

from core.cgg import Node
from core.controller import Controller
from core.world import World


class Persistence:
    default_folder_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "..", "output")
    )

    @staticmethod
    def dump_cgg(cgg: Node, folder_path: str = None):

        if folder_path is None:
            folder_path = Persistence.default_folder_path

        output_file = f"{folder_path}/cgg.dat"

        folder_path = Path(folder_path)
        output_file = Path(output_file)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        with open(output_file, "wb") as out_strm:
            dill.dump(cgg, out_strm)

    @staticmethod
    def dump_world(world: World, folder_path: str = None):

        if folder_path is None:
            folder_path = Persistence.default_folder_path

        output_file = f"{folder_path}/world.dat"

        output_file = Path(output_file)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        file = open(output_file, "wb")
        dill.dump(world, file)
        file.close()

    @staticmethod
    def dump_goals(set_goals: Set[Node], folder_path: str = None):

        if folder_path is None:
            folder_path = Persistence.default_folder_path

        output_file = f"{folder_path}/goals.dat"

        output_file = Path(output_file)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        file = open(output_file, "wb")
        dill.dump(set_goals, file)
        file.close()

    @staticmethod
    def dump_controller(
        controller: Controller, folder_path: str = None, name: str = None
    ):

        if name is None:
            name = "controller"

        output_file = f"{folder_path}/{name}.dat"

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        output_file = Path(output_file)

        file = open(output_file, "wb")
        dill.dump(controller, file)
        file.close()

    @staticmethod
    def load_cgg(folder_path: str) -> Node:

        file = f"{folder_path}/cgg.dat"

        file = Path(file)

        file = open(file, "rb")
        cgg = dill.load(file)
        file.close()

        return cgg

    @staticmethod
    def load_controller(folder_path: str, name: str = None) -> Controller:

        if name is None:
            file = f"{folder_path}/controller.dat"
        else:
            file = f"{folder_path}/{name}.dat"

        file = Path(file)

        file = open(file, "rb")
        controller = dill.load(file)
        file.close()

        return controller

    @staticmethod
    def load_world(folder_path: str) -> World:

        file = f"{folder_path}/world.dat"

        file = Path(file)

        file = open(file, "rb")
        world = dill.load(file)
        file.close()

        return world

    @staticmethod
    def load_goals(folder_path: str) -> Set[Node]:

        file = f"{folder_path}/goals.dat"

        file = Path(file)

        # Added this
        if not os.path.exists(file):
            Persistence.dump_goals(set(), folder_path)
        # Added this

        file = open(file, "rb")
        set_goals = dill.load(file)
        file.close()

        return set_goals
