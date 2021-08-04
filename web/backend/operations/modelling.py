import json
import os
from os import walk
from pathlib import Path
from typing import Set

from cgg import Node
from specification.atom.pattern.robotics.coremovement.surveillance import *
from specification.formula import Formula
from tools.persistence import Persistence
from typeset import Typeset
from world import World


class Modelling:

    @staticmethod
    def create_environment(project_folder):

        with open(Path(os.path.join(project_folder, "environment.json"))) as json_file:
            json_obj = json.load(json_file)

        w = World(project_name=json_obj["project_id"])
        for action in json_obj["actions"]:
            if action["mutex_group"]:
                w.new_boolean_action(action["name"], mutex=action["mutex_group"])
            else:
                w.new_boolean_action(action["name"])
        for sensor in json_obj["sensors"]:
            if sensor["mutex_group"]:
                w.new_boolean_sensor(sensor["name"], mutex=sensor["mutex_group"])
            else:
                w.new_boolean_sensor(sensor["name"])
        for location in json_obj["grid"]["locations"]:
            w.new_boolean_location(location["id"], mutex="locations", adjacency=location["adjacency"])
        w.new_boolean_context("day", mutex="time")
        w.new_boolean_context("night", mutex="time")

        Persistence.dump_world(w, project_folder)

    @staticmethod
    def add_goal(project_folder):
        set_of_goals = Modelling.get_goals(project_folder)

        # TODO: Mockup - Fix me

        w = Persistence.load_world(project_folder)

        # CASE 1: designer inserted a LTL formula, i.e. a string on some world variables
        ltl_formula = Formula(Atom(formula=("G(F(r1 & r2))", Typeset({w["r1"], w["r1"]}))))

        new_goal = Node(name="Day patrolling",
                          description="description",
                          specification=ltl_formula)

        set_of_goals.add(new_goal)


        # CASE 2: designer has inserted a patter:
        pattern_formula = StrictOrderedPatrolling([w["r1"], w["r2"]])

        new_goal = Node(name="Day patrolling 2",
                          description="description",
                          specification=pattern_formula)

        set_of_goals.add(new_goal)

        Persistence.dump_goals(set_of_goals, project_folder)



    @staticmethod
    def get_goals(project_folder) -> Set[Node]:
        set_of_goals = Persistence.load_goals(project_folder)
