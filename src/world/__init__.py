from specification import Specification
from specification.atom import Atom
from type.subtypes.active import Active
from typing import Set, Dict, Tuple
from type import Types
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
                 actions: Set[Types] = None,
                 locations: Set[Types] = None,
                 sensors: Set[Types] = None,
                 contexts: Set[Types] = None):
        super().__init__()

        self.__typeset = Typeset(actions | locations | sensors | contexts | {Active()})

        for name, elem in self.__typeset.items():
            super(World, self).__setitem__(name, elem.to_atom())
            super(World, self).__setitem__(f"!{name}", ~elem.to_atom())

        self.__rules: Set[Rule] = set()

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
