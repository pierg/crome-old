import json
import os
from os import walk
from pathlib import Path
from typing import Set

from cgg import Node
from contract import Contract
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
    def add_goal_updated(project_folder):

        """Load existing list of goals objects and world"""
        set_of_goals = Persistence.load_goals(project_folder)
        w = Persistence.load_world(project_folder)

        """Create a new goal"""

        """Assumptions (if inserted by the designer"""
        a1 = Formula(Atom(formula=("G(F(r1 & r2))", Typeset({w["r1"], w["r1"]}))))
        a2 = Patrolling([w["r1"], w["r2"]])

        """Guarantees"""
        g1 = Formula(Atom(formula=("G(F(r3 & r4))", Typeset({w["r3"], w["r4"]}))))
        g2 = StrictOrderedPatrolling([w["r1"], w["r2"]])

        """Context"""
        context = w["day"]

        contract = Contract(
            assumptions=a1 & a2,
            guarantees=g1 & g2
        )

        """Instanciate the goal"""

        new_goal = Node(name="Day patrolling",
                        description="description",
                        specification=contract,
                        context=context,
                        world=w)

        set_of_goals.add(new_goal)

        Persistence.dump_goals(set_of_goals, project_folder)

    @staticmethod
    def add_goal(project_folder):
        set_of_goals = Persistence.load_goals(project_folder)

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
    def get_goals(project_folder) -> str:
        set_of_goals = Persistence.load_goals(project_folder)
