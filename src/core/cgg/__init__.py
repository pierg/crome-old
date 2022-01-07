from __future__ import annotations

import itertools
import json
import os
import random
from copy import deepcopy
from enum import Enum, auto
from pathlib import Path
from typing import TYPE_CHECKING, Dict, List, Set, Tuple, Union

from tabulate import tabulate

from core.cgg.exceptions import CGGFailOperations, CGGOperationFail, TransSynthesisFail
from core.contract import Contract
from core.controller import Controller
from core.controller.exceptions import ControllerException
from core.crometypes import Types
from core.crometypes.subtypes.location import ReachLocation
from core.goal import Goal
from core.goal.exceptions import GoalException
from core.specification import Specification, SpecNotSATException
from core.typeset import Typeset
from tools.logic import Logic
from tools.storage import Store
from tools.strings import StringMng

if TYPE_CHECKING:
    from core.world import World

from tools.strix import Strix


class Link(Enum):
    REFINEMENT = 0
    COMPOSITION = 1
    CONJUNCTION = 2
    DISJUNCTION = 3
    MERGING = 4
    QUOTIENT = 5
    SEPARATION = 6


class GraphTraversal(Enum):
    DFS = auto()
    BFS = auto()


class Node(Goal):
    def __init__(
        self,
        name: str = None,
        description: str = None,
        id: str = None,
        specification: Union[Specification, Contract] = None,
        context: Specification = None,
        world: World = None,
        viewpoint: str = None,
        goal: Goal = None,
    ):
        """Graph properties."""

        if goal is None:
            super().__init__(
                name, description, id, specification, context, world, viewpoint
            )
        elif (
            goal is not None
            and name is None
            and description is None
            and specification is None
            and context is None
            and world is None
            and viewpoint is None
        ):
            super().__init__(
                goal.name,
                goal.description,
                goal.id,
                goal.specification,
                goal.context,
                goal.world,
                goal.viewpoint,
            )
        else:
            raise AttributeError

        """Dictionary Link -> Set[Node]"""
        self.__parents = {}

        """Dictionary Link -> Set[Node]"""
        self.__children = {}

        self.__cgg_folder_name = f"cgg_root_{self.id}"

        self.__t_trans: int = 0
        self.__t_controllers: Dict[Tuple[ReachLocation, ReachLocation], Controller] = {}

    def __str__(self, level=0):
        """Print current Goal."""
        ret = Goal.pretty_print_goal(self, level)

        if self.children is not None:

            for link, goals in self.children.items():

                ret += "\t" * level + "|  " + link.name + "\n"
                level += 1
                for child in goals:
                    try:
                        ret += child.__str__(level + 1)
                    except:
                        print("ERROR IN PRINT")
        return ret

    def set_session_name(
        self,
        value: str,
        traversal: GraphTraversal = GraphTraversal.DFS,
        explored: Set[Node] = None,
        root=None,
    ):
        """Set session name to all nodes of the CGG."""

        if root is None:
            root = self

        if explored is None:
            explored = set()

        if traversal == GraphTraversal.DFS:
            """Dept-First Search."""
            """Label current node as explored"""
            explored.add(self)
            for node in self.children_nodes():
                if node not in explored:
                    node.set_session_name(value, traversal, explored, root)

            self.session_name = value

        if traversal == GraphTraversal.BFS:
            raise NotImplemented

    @property
    def t_trans(self) -> int:
        return self.__t_trans

    @property
    def t_controllers(self) -> Dict[Tuple[ReachLocation, ReachLocation], Controller]:
        """Returns all transition controllers."""
        return self.__t_controllers

    @property
    def t_controllers_folder_name(self) -> str:
        return "t_controllers"

    @property
    def parents(self) -> Dict[Link, Set[Node]]:
        return self.__parents

    @property
    def children(self) -> Dict[Link, Set[Node]]:
        return self.__children

    @property
    def storage_file(self):

        output_file = f"{Store.output_folder}/cgg.dat"

        if not os.path.exists(Store.output_folder):
            os.makedirs(Store.output_folder)

        return open(output_file, "wb")

    def add_parents(self, link: Link, nodes: Set[Node]):
        if link in self.__parents.keys():
            self.__parents[link] |= nodes
        else:
            self.__parents[link] = nodes

    def add_children(self, link: Link, nodes: Set[Node]):
        if link == Link.COMPOSITION or link == Link.CONJUNCTION:
            if link in self.__children.keys():
                raise Exception(
                    "A composition/conjunction children link already exists!"
                )
            self.__children[link] = nodes
        else:
            """Link.REFINEMENT."""
            if link in self.__children.keys():
                self.__children[link] |= nodes
            else:
                self.__children[link] = nodes
        for goal in self.__children[link]:
            goal.add_parents(link=link, nodes={self})

    def parents_nodes(self) -> Set[Node]:
        ret = set()
        if len(self.__parents) > 0:
            for link, values in self.__parents.items():
                ret |= values
        return ret

    def children_nodes(self) -> Set[Node]:
        ret = set()
        if len(self.__children) > 0:
            for link, values in self.__children.items():
                ret |= values
        return ret

    def translate_all_to_buchi(
        self,
        traversal: GraphTraversal = GraphTraversal.DFS,
        explored: Set[Node] = None,
        root=None,
    ):
        """Realize all nodes of the CGG."""

        if root is None:
            root = self

        if explored is None:
            explored = set()

        if traversal == GraphTraversal.DFS:
            """Dept-First Search."""
            """Label current node as explored"""
            explored.add(self)
            for node in self.children_nodes():
                if node not in explored:
                    node.translate_all_to_buchi(traversal, explored, root)

            self.translate_to_buchi()

        if traversal == GraphTraversal.BFS:
            raise NotImplemented

    def get_scenarios(self) -> Set[Node]:
        if Link.CONJUNCTION in self.children:
            return self.children[Link.CONJUNCTION]
        else:
            return {self}

    def refine_by(self, goal: Node):
        pass

    def orchestrate(self, n_steps: int, t_min_context: int = 10):
        if t_min_context < self.t_trans:
            raise Exception("T context min < T transition max")

        scenarios = self.get_scenarios()
        active_scenario = random.sample(scenarios, 1)[0]

        headers = ["t", "context", "controller", "inputs", "outputs"]
        history: List[List[str]] = []

        """Counter for how long the current context has been active"""
        active_context_count = 0
        """Context switch probability, it will be linearly increased up to 0.9"""
        cs_prob = 0.2
        current_t = 0
        while current_t < n_steps:
            context_switch = False
            if active_context_count >= t_min_context and len(scenarios) > 1:
                """Calculating context-switch probability."""
                if cs_prob < 0.9:
                    cs_prob = cs_prob + 0.05 * (active_context_count - t_min_context)
                context_switch = random.choices([True, False], [cs_prob, 1 - cs_prob])[
                    0
                ]
            if context_switch:
                new_scenario = random.sample(scenarios, 1)[0]
                while new_scenario is active_scenario:
                    new_scenario = random.sample(scenarios, 1)[0]

                start = active_scenario.controller.current_location
                destination = new_scenario.controller.next_location_to_visit

                """Locations adjacent to destination"""
                adjacent_locations = self.world.adjacent_types(destination)

                """Set new active scenario"""
                active_scenario = new_scenario
                active_context_count = 0
                cs_prob = 0.2

                """Choose the destination reachable in the least number of steps"""
                n_states = None
                optimal_destination = None
                for destination in adjacent_locations:
                    if n_states is None:
                        if (start, destination) in self.__t_controllers:
                            n_states = len(
                                self.__t_controllers[(start, destination)].states
                            )
                            optimal_destination = destination
                    else:
                        if (start, destination) in self.__t_controllers:
                            if (
                                len(self.__t_controllers[(start, destination)].states)
                                < n_states
                            ):
                                n_states = len(
                                    self.__t_controllers[(start, destination)].states
                                )
                                optimal_destination = destination
                t_ctrl = self.__t_controllers[(start, optimal_destination)]
                ctrl_str = t_ctrl.name

                """First reaction is already been made by the previous controller"""
                inputs, outputs = t_ctrl.react()
                active_location = None
                for x in outputs:
                    from core.specification import AtomKind

                    if x.kind == AtomKind.LOCATION and not x.negated:
                        active_location = x
                while (
                    list(active_location.typeset.values())[0] is not optimal_destination
                ):
                    inputs, outputs = t_ctrl.react()
                    active_context_count += 1
                    active_location = None
                    for x in outputs:
                        if x.kind == AtomKind.LOCATION and not x.negated:
                            active_location = x
                    context_str = active_scenario.context.string
                    outputs_str = []
                    for x in outputs:
                        if not x.negated:
                            outputs_str.append(str(x))
                    outputs_str = ", ".join(outputs_str)
                    # print(f"{i}\t{context_str}\t\t{outputs_str}")
                    history.append([current_t, context_str, ctrl_str, "", outputs_str])
                    current_t += 1
                """Destination Reached"""
                """Reset transition controller and activate new scenario"""
                t_ctrl.reset()

            s_ctrl = active_scenario.controller
            ctrl_str = s_ctrl.name
            """Take a step"""
            inputs, outputs = s_ctrl.react()
            active_context_count += 1
            if active_scenario.context is not None:
                context_str = active_scenario.context.string
            else:
                context_str = "true"
            inputs_str = []
            for x in inputs:
                if not x.negated:
                    inputs_str.append(str(x))
            outputs_str = []
            for x in outputs:
                if not x.negated:
                    outputs_str.append(str(x))
            inputs_str = ", ".join(inputs_str)
            outputs_str = ", ".join(outputs_str)
            # print(f"{i}\t{context_str}\t{inputs_str}\t{outputs_str}")
            print(
                "\t".join(
                    [
                        str(current_t),
                        str(context_str),
                        str(ctrl_str),
                        str(inputs_str),
                        str(outputs_str),
                    ]
                )
            )
            history.append([current_t, context_str, ctrl_str, inputs_str, outputs_str])
            current_t += 1

        return tabulate(history, headers=headers)

    def realize_all(self, t_trans: int):
        """Realize Sepcification and Transition Controllers."""
        self.realize_specification_controllers()
        self.realize_transition_controllers(t_trans)

    def realize_transition_controllers(self, t_trans_max: int):
        self.__t_trans = t_trans_max
        scenarios = self.get_scenarios()

        if scenarios is None:
            print("Realize Transition Controllers: No CGG found")
            return

        """Context -> Specification Controllers"""
        s_controllers: Dict[Specification, Controller] = {}
        for scenario in scenarios:
            s_controllers[scenario.context] = scenario.controller
        self.__t_controllers: Dict[Tuple[ReachLocation, ReachLocation], Controller] = {}

        """Generating Transition Controllers"""
        for scenario_a, scenario_b in itertools.combinations(scenarios, 2):
            # locs_a = scenario_a.controller.locations
            # locs_b = scenario_a.controller.locations
            #  TODO
            # for loc_source, loc_target in itertools.product(locs_a, locs_b):
            #
            scenario_a_entry_points = scenario_a.controller.all_entry_locations(
                self.world.typeset
            )
            scenario_b_entry_points = scenario_b.controller.all_entry_locations(
                self.world.typeset
            )
            #
            # scenario_a_entry_points = scenario_a.controller.locations
            # scenario_b_entry_points = scenario_b.controller.locations

            print(", ".join([x.name for x in scenario_a_entry_points]))
            print(", ".join([x.name for x in scenario_b_entry_points]))
            for start, finish in itertools.product(
                scenario_a_entry_points, scenario_b_entry_points
            ):
                if start == finish:
                    continue
                self.__t_controllers[
                    (start, finish)
                ] = self.create_transition_controller(start, finish, t_trans_max)
                self.__t_controllers[
                    (finish, start)
                ] = self.create_transition_controller(finish, start, t_trans_max)

        print(f"{len(self.__t_controllers)} transition controller_specs generated:")
        for start, finish in self.__t_controllers.keys():
            print(f"{start.name} -> {finish.name}")

    def realize_specification_controllers(
        self,
        traversal: GraphTraversal = GraphTraversal.DFS,
        explored: Set[Node] = None,
        root=None,
    ):
        """Realize all nodes of the CGG."""

        if root is None:
            root = self

        if explored is None:
            explored = set()

        if traversal == GraphTraversal.DFS:
            """Dept-First Search."""
            """Label current node as explored"""
            explored.add(self)
            for node in self.children_nodes():
                if node not in explored:
                    node.realize_specification_controllers(traversal, explored, root)

            self.realize_to_controller()

        if traversal == GraphTraversal.BFS:
            raise NotImplemented

    def get_all_nodes(self) -> Set[Node]:

        """Depth-first search."""
        result = set()
        result.add(self)
        for child in self.children_nodes():
            result |= child.get_all_nodes()
        return result

    def get_leaves(self) -> Set[Node]:
        """Depth-first search."""
        result = set()
        if len(self.children) == 0:
            result.add(self)
        for child in self.children_nodes():
            result |= child.get_all_nodes()
        return result

    def save(self):
        Store.save_to_file(str(self), "cgg.txt", self.session_name)

    def export_to_json(self, goals_folder: str):
        self.rec_exporting_to_json(goals_folder)

    def rec_exporting_to_json(self, goals_folder: str, parent_goal_id: str = None):
        if len(self.children) != 0:
            copy = {"goal": self.name, "id": self.id}
            for link, goals in self.children.items():
                copy["link"] = link.name
                copy["children"] = []
                for goal in goals:
                    child = goal.rec_exporting_to_json(goals_folder, self.id)
                    Node.exporting_in_files(
                        self.id,
                        goals_folder,
                        "children",
                        child["id"],
                        self.name,
                        link.name,
                    )
                    copy["children"].append(child)
            return copy
        if parent_goal_id is not None:
            Node.exporting_in_files(
                self.id, goals_folder, "parents", parent_goal_id, self.name
            )
        return {"goal": self.name, "id": self.id}

    @staticmethod
    def exporting_in_files(
        node_id: str,
        goals_folder: str,
        mode: str,
        new_element: str,
        goal_name: str,
        link: str = None,
    ):
        filename = str(node_id).split("-")
        goal_folder = Path(
            os.path.join(goals_folder, f"{filename[len(filename) - 1].zfill(4)}.json")
        )
        if os.path.exists(goal_folder):
            with open(goal_folder) as json_file:
                json_goal = json.load(json_file)
        else:
            json_goal = {"group": "new", "name": goal_name, "id": node_id}
        with open(goal_folder, "w") as json_file:
            existing_array = []
            if mode in json_goal:
                for element in json_goal[mode]:
                    existing_array.append(element)
            if new_element not in existing_array:
                existing_array.append(new_element)
            if link is not None:
                json_goal["link"] = link
            json_goal[mode] = existing_array
            json_formatted = json.dumps(json_goal, indent=4, sort_keys=True)
            json_file.write(json_formatted)

    def create_transition_controller(
        self, start: Types, finish: Types, t_trans: int
    ) -> Controller:

        t_controller_name = f"TRANS_{start.name}-{finish.name}"

        if self.session_name is None:
            folder_name = f"{self.t_controllers_folder_name}/{t_controller_name}"
        else:
            folder_name = f"{self.session_name}/{self.t_controllers_folder_name}/{t_controller_name}"

        typeset = Typeset({start, finish})
        realizable = False
        for n_steps in range(1, t_trans):
            trans_spec_str = Logic.and_([start.name, Logic.xn_(finish.name, n_steps)])
            trans_spec = Atom(formula=(trans_spec_str, typeset))
            trans_contract = Contract(guarantees=trans_spec)
            try:
                controller_info = trans_contract.get_controller_info(
                    world_ts=self.world.typeset
                )
                a, g, i, o = controller_info.get_strix_inputs()
                controller_synthesis_input = StringMng.get_controller_synthesis_str(
                    controller_info
                )
                Store.save_to_file(
                    controller_synthesis_input,
                    f"t_controller_{start.name}_{finish.name}_specs.txt",
                    folder_name,
                )
                realized, kiss_mealy, time = Strix.generate_controller(a, g, i, o)
                if realized:
                    realizable = True
                    break
            except ControllerException as e:
                raise TransSynthesisFail(self, e)
        if not realizable:
            raise Exception(
                f"Controller [{start.name}, {finish.name}] cannot be synthetized in {t_trans} steps"
            )
        else:
            Store.save_to_file(
                kiss_mealy, f"{start.name}_{finish.name}_mealy", folder_name
            )
            # Store.generate_eps_from_dot(dot_mealy, f"{start.name}_{finish.name}_dot",
            #                             folder_name)

            t_controller = Controller(
                mealy_machine=kiss_mealy,
                world=self.world,
                name=t_controller_name,
                synth_time=time,
            )
            Store.save_to_file(
                str(t_controller), f"{start.name}_{finish.name}_table", folder_name
            )

            return t_controller

    @staticmethod
    def composition(
        nodes: Set[Node], name: str = None, description: str = None
    ) -> Node:

        try:
            new_goal = Goal.composition(nodes, name, description)
        except GoalException as e:
            raise CGGOperationFail(
                nodes=nodes, operation=CGGFailOperations.algebra_op, goal_ex=e
            )

        new_node = Node(goal=new_goal)

        new_node.add_children(link=Link.COMPOSITION, nodes=set(nodes))

        return new_node

    @staticmethod
    def conjunction(
        nodes: Set[Node], name: str = None, description: str = None
    ) -> Node:

        try:
            new_goal = Goal.conjunction(nodes, name, description)
        except GoalException as e:
            raise CGGOperationFail(
                nodes=nodes, operation=CGGFailOperations.algebra_op, goal_ex=e
            )

        new_node = Node(goal=new_goal)

        new_node.add_children(link=Link.CONJUNCTION, nodes=nodes)

        return new_node

    @staticmethod
    def merging(nodes: Set[Node], name: str = None, description: str = None) -> Node:

        try:
            new_goal = Goal.merging(nodes, name, description)
        except GoalException as e:
            raise CGGOperationFail(
                nodes=nodes, operation=CGGFailOperations.algebra_op, goal_ex=e
            )

        new_node = Node(goal=new_goal)

        new_node.add_children(link=Link.MERGING, nodes=nodes)

        return new_node

    def quotient(self, divisor: Node) -> Node:

        dividend = self

        try:
            new_goal = Goal.quotient(dividend, divisor)
        except GoalException as e:
            raise CGGOperationFail(
                nodes={dividend, divisor},
                operation=CGGFailOperations.algebra_op,
                goal_ex=e,
            )

        new_node = Node(goal=new_goal)

        """TODO: differenciate between dividend and divisor"""
        new_node.add_children(link=Link.QUOTIENT, nodes={dividend, divisor})

        return new_node

    def separation(self, divisor: Node) -> Node:

        dividend = self

        try:
            new_goal = Goal.separation(dividend, divisor)
        except GoalException as e:
            raise CGGOperationFail(
                nodes={dividend, divisor},
                operation=CGGFailOperations.algebra_op,
                goal_ex=e,
            )

        new_node = Node(goal=new_goal)

        """TODO: differenciate between dividend and divisor"""
        new_node.add_children(link=Link.SEPARATION, nodes={dividend, divisor})

        return new_node

    @staticmethod
    def disjunction(
        nodes: Set[Node], name: str = None, description: str = None
    ) -> Node:

        try:
            new_goal = Goal.disjunction(nodes, name, description)
        except GoalException as e:
            raise CGGOperationFail(
                nodes=nodes, operation=CGGFailOperations.algebra_op, goal_ex=e
            )

        new_node = Node(goal=new_goal)

        new_node.add_children(link=Link.DISJUNCTION, nodes=nodes)

        return new_node

    @staticmethod
    def build_cgg(nodes: Set[Node]) -> Node:

        contexts = set()

        for g in nodes:
            if g.context is not None:
                contexts.add(g.context)

        """Extract all combinations of context which are consistent"""
        saturated_combinations = []
        print([c for c in contexts])
        combinations = itertools.combinations(contexts, (0 + 1) % (len(contexts)))
        for combination in combinations:
            print(f"Combination\t{str([str(e) for e in combination])}")
        for i in range(0, len(contexts)):
            """Extract all combinations of i context and saturate it."""
            combinations = itertools.combinations(contexts, (i + 1) % (len(contexts)))
            for combination in combinations:
                if len(combination) == 0:
                    continue
                print(f"Selected\t{str([str(e) for e in combination])}")
                saturated_combination = deepcopy(combination[0])
                for element in combination[1:]:
                    saturated_combination &= element
                print(f"Conjoined\t{saturated_combination}")
                for context in contexts:
                    print(f"Context\t{context}")
                    if context not in combination:
                        saturated_combination &= ~context
                        print(f"Saturated\t{saturated_combination}")
                if not saturated_combination.is_satisfiable:
                    continue
                else:
                    saturated_combinations.append(saturated_combination)
                    print(f"Added\t{saturated_combination}")

        print("\n".join(x.string for x in saturated_combinations))

        """Group combinations"""
        saturated_combinations_grouped = list(saturated_combinations)
        for c_a in saturated_combinations:
            for c_b in saturated_combinations:
                if (
                    c_a is not c_b
                    and c_a <= c_b
                    and c_b in saturated_combinations_grouped
                ):
                    saturated_combinations_grouped.remove(c_b)

        print("\n".join(x.string for x in saturated_combinations))

        """Map to goals"""
        mapped_goals = set()
        context_goal_map: Dict[Specification, Dict[str, Set[Node]]] = {}
        for goal in nodes:
            for combination in saturated_combinations_grouped:
                add_goal = False
                if goal.context is not None:
                    print(f"{str(combination)} <= {str(goal.context)}")
                    if combination <= goal.context:
                        add_goal = True
                else:
                    add_goal = True
                if add_goal:
                    if combination in context_goal_map:
                        if goal.viewpoint in context_goal_map[combination]:
                            context_goal_map[combination][goal.viewpoint].add(goal)
                        else:
                            context_goal_map[combination][goal.viewpoint] = {goal}
                    else:
                        context_goal_map[combination] = dict()
                        context_goal_map[combination][goal.viewpoint] = {goal}
                    mapped_goals.add(goal)

        if mapped_goals != nodes:
            raise Exception("Not all goals have been mapped!")
        print("All goals have been mapped to mutually exclusive context")

        """Building the cgg..."""
        merged_goals = set()
        for mutex_context, cluster in context_goal_map.items():
            composed_goals = set()
            for viewpoint, goals in cluster.items():
                new_node = Node.composition(cluster[viewpoint])
                new_node.context = mutex_context
                composed_goals.add(new_node)
            new_node = Node.merging(composed_goals)
            new_node.context = mutex_context
            merged_goals.add(new_node)

        cgg = Node.conjunction(merged_goals)

        """Assigning names for each node as 'scenarios'"""
        for i, node in enumerate(cgg.get_scenarios()):
            node.name = f"SCENARIO_{i}"
        cgg.name = "MISSION"

        return cgg

    @staticmethod
    def build_cgg_old(nodes: Set[Node], kind: Link = Link.CONJUNCTION) -> Node:

        contexts = set()

        for g in nodes:
            if g.context is not None:
                contexts.add(g.context)

        """Extract all combinations of context which are consistent"""
        saturated_combinations = []
        for i in range(0, len(contexts)):
            """Extract all combinations of i context and saturate it."""
            combinations = itertools.combinations(contexts, i + 1)
            for combination in combinations:
                saturated_combination = combination[0]
                try:
                    for element in combination[1:]:
                        saturated_combination &= element
                    for context in contexts:
                        if context not in combination:
                            saturated_combination &= ~context
                except SpecNotSATException:
                    continue
                saturated_combinations.append(saturated_combination)

        print("\n".join(x.string for x in saturated_combinations))

        """Group combinations"""
        saturated_combinations_grouped = list(saturated_combinations)
        for c_a in saturated_combinations:
            for c_b in saturated_combinations:
                if (
                    c_a is not c_b
                    and c_a <= c_b
                    and c_b in saturated_combinations_grouped
                ):
                    saturated_combinations_grouped.remove(c_b)

        print("\n".join(x.string for x in saturated_combinations))

        """Map to goals"""
        mapped_goals = set()
        context_goal_map: Dict[Specification, Set[Node]] = {}
        for goal in nodes:
            if goal.context is not None:
                for combination in saturated_combinations_grouped:
                    if combination <= goal.context:
                        if combination in context_goal_map:
                            context_goal_map[combination].add(goal)
                        else:
                            context_goal_map[combination] = {goal}
                        mapped_goals.add(goal)
            else:
                for combination in saturated_combinations_grouped:
                    if combination in context_goal_map:
                        context_goal_map[combination].add(goal)
                    else:
                        context_goal_map[combination] = {goal}
                    mapped_goals.add(goal)

        if mapped_goals != nodes:
            raise Exception("Not all goals have been mapped!")
        print("All goals have been mapped to mutually exclusive context")

        """Building the cgg..."""
        composed_goals = set()
        for mutex_context, cluster in context_goal_map.items():
            new_node = Node.composition(cluster)
            new_node.context = mutex_context
            composed_goals.add(new_node)

        if kind == Link.CONJUNCTION:
            cgg = Node.conjunction(composed_goals)
        elif kind == Link.DISJUNCTION:
            cgg = Node.disjunction(composed_goals)
        else:
            cgg = Node.conjunction(composed_goals)

        """Renaming the CGG Mission and Scenarios nodes"""

        """Assigning names for each node as 'scenarios'"""
        for i, node in enumerate(cgg.get_scenarios()):
            node.name = f"SCENARIO_{i}"
        cgg.name = "MISSION"

        return cgg
