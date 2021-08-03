import uuid

from specification import Specification
from specification.atom import Atom
from type.subtypes.action import BooleanAction
from type.subtypes.active import Active
from typing import Set, Dict, Tuple
from type import Types
from type.subtypes.context import ContextBoolean
from type.subtypes.sensor import BooleanSensor
from typeset import Typeset

from typing import TYPE_CHECKING

from type.subtypes.location import ReachLocation


class Rule:
    def __init__(self,
                 rule: Specification,
                 trigger: Specification = None,
                 description: str = None,
                 system: bool = True
                 ):
        self.__rule = rule
        self.__trigger = trigger
        self.__description = description
        self.__system = system

    @property
    def rule(self):
        return self.__rule

    @property
    def trigger(self):
        return self.__trigger

    @property
    def description(self):
        return self.__description

    @property
    def system(self):
        return self.__system


class World(dict):
    """"Instanciate atomic propositions (and their negation) for each Type"""

    def __init__(self,
                 project_name: str = None,
                 actions: Set[Types] = None,
                 locations: Set[Types] = None,
                 sensors: Set[Types] = None,
                 contexts: Set[Types] = None):
        super().__init__()

        if project_name is None:
            self.__project_name = uuid.uuid4()
        else:
            self.__project_name = project_name

        self.__typeset = Typeset()

        # self.__typeset = Typeset(actions | locations | sensors | contexts | {Active()})

        if actions is not None:
            self.__typeset |= Typeset(actions)

        if locations is not None:
            self.__typeset |= Typeset(locations)

        if sensors is not None:
            self.__typeset |= Typeset(sensors)

        if contexts is not None:
            self.__typeset |= Typeset(contexts)

        for name, elem in self.__typeset.items():
            super(World, self).__setitem__(name, elem.to_atom())
            super(World, self).__setitem__(f"!{name}", ~elem.to_atom())

        self.__rules: Set[Rule] = set()

    def add_type(self, name, elem: Types):
        self.__typeset |= elem
        super(World, self).__setitem__(name, elem.to_atom())
        super(World, self).__setitem__(f"!{name}", ~elem.to_atom())

    def new_boolean_action(self, name, mutex: str = None):
        elem = BooleanAction(name, mutex)
        self.add_type(name, elem)

    def new_boolean_sensor(self, name, mutex: str = None):
        elem = BooleanSensor(name, mutex)
        self.add_type(name, elem)

    def new_boolean_location(self, name, mutex: str = None, adjacency: Set[str] = None):
        elem = ReachLocation(name, mutex, adjacency)
        self.add_type(name, elem)

    def new_boolean_context(self, name, mutex: str = None):
        elem = ContextBoolean(name, mutex)
        self.add_type(name, elem)

    @property
    def project_name(self) -> str:
        return self.__project_name

    @property
    def rules(self) -> Set[Rule]:
        return self.__rules

    @property
    def typeset(self) -> Typeset:
        return self.__typeset

    def add_rules(self, rules: Set[Rule]):
        self.__rules |= rules

    def adjacent_types(self, location: ReachLocation) -> Set[ReachLocation]:

        adjacent_types = set()
        for class_name in location.adjacency_set:
            for t in self.typeset.values():
                if type(t).__name__ == class_name:
                    adjacent_types.add(t)

        return adjacent_types
