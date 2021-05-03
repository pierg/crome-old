from specification import Specification
from type.subtypes.active import Active
from typing import Set
from type import Types
from typeset import Typeset


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

        self.__rules = set()

    @property
    def rules(self) -> Set[Specification]:
        return self.__rules

    @property
    def typeset(self) -> Typeset:
        return self.__typeset

    def add_rules(self, rules: Set[Specification]):
        for rule in rules:
            self.__rules |= rule
