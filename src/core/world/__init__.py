import uuid
from typing import Set

from core.crometypes import CTypes
from core.crometypes.subtypes.action import BooleanAction
from core.crometypes.subtypes.context import ContextBoolean
from core.crometypes.subtypes.location import ReachLocation
from core.crometypes.subtypes.sensor import BooleanSensor
from core.specification import Specification
from core.typeset import Typeset


class Rule:
    def __init__(
        self,
        rule: Specification,
        trigger: Specification = None,
        description: str = None,
        system: bool = True,
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
    """"Instanciate atomic propositions (and their negation) for each Type."""

    def __init__(
        self,
        project_name: str = None,
        actions: Set[CTypes] = None,
        locations: Set[CTypes] = None,
        sensors: Set[CTypes] = None,
        contexts: Set[CTypes] = None,
    ):
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
            super().__setitem__(name, elem.to_atom())
            elem.to_atom()
            super().__setitem__(f"!{name}", ~elem.to_atom())

        self.__rules: Set[Rule] = set()

    def add_type(self, name, elem: CTypes):
        self.__typeset |= elem
        super().__setitem__(name, elem.to_atom())
        super().__setitem__(f"!{name}", ~elem.to_atom())

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

    def equals(self, world) -> bool:
        return self.typeset == world.typeset
