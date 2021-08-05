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
        # g3 = InstantaneousReaction() // need to import every pattern method ?

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
    def add_goal(project_folder, goal_id):
        set_of_goals = Persistence.load_goals(project_folder)

        w = Persistence.load_world(project_folder)

        goal_path = Path(os.path.join(project_folder, f"goals/{str(goal_id).zfill(4)}.json"))

        with open(goal_path) as json_file:
            json_obj = json.load(json_file)
            contract_names = ["assumptions", "guarantees"]
            contract_lists = [[], []]
            for i in range(len(contract_lists)):
                for contract_element in json_obj["contract"][contract_names[i]]:
                    if "pattern" in contract_element:
                        args = contract_element["pattern"]["arguments"]
                        if "format" in args & args["format"] == "list":
                            list_of_locations = []
                            for location in args["value"]:
                                list_of_locations.append(w[location])
                            contract_lists[i].append(contract_element["pattern"]["name"](list_of_locations))
                        else:
                            contract_lists[i].append(contract_element["pattern"]["name"](args["value"]))
                    elif "ltl_value" in contract_element:
                        if "world_values" in contract_element:
                            values = []
                            for array in contract_element["world_values"]:
                                for value in array:
                                    values.append(w[value])
                            contract_lists[i].append(Formula(Atom(formula=(contract_element["ltl_value"],
                                                                           Typeset({w["r1"], w["r2"]})))))
                            # TODO FIX FOR PIER
                            # we have to change w["r1"], w["r2"] by the real array called values which
                            # contains the real used locations/actions/sensors of the LTL
                            # TODO FIX FOR PIER

            context = w["day"]

            lists_with_and_operators = []
            for i in range(len(contract_lists)):
                lists_with_and_operators.append(None)
                for j in range(len(contract_lists[i])):
                    if j == 0:
                        lists_with_and_operators[i] = contract_lists[i][0]
                    else:
                        lists_with_and_operators[i] = lists_with_and_operators[i] & contract_lists[i][j]

            print("LISTS WITH OPERATORS")
            print(lists_with_and_operators)

            contract = Contract(
                assumptions=lists_with_and_operators[0],
                guarantees=lists_with_and_operators[1]
            )

            new_goal = Node(name="Day patrolling",
                            description="description",
                            specification=contract,
                            context=context,
                            world=w)

            set_of_goals.add(new_goal)

            Persistence.dump_goals(set_of_goals, project_folder)
