from specification import Specification
from type.subtypes.active import Active
from typing import Set
from type import Types
from typeset import Typeset


class World(dict):
    def __init__(self, actions: Set[Types] = None, locations: Set[Types] = None, sensors: Set[Types] = None,
                 contexts: Set[Types] = None, rules: Set[Specification] = None):
        super().__init__()

        self.__typeset = Typeset(actions | locations | sensors | contexts | {Active()})

        for name, elem in self.__typeset.items():
            super(World, self).__setitem__(name, elem.to_atom())

        self.__rules = rules

    @property
    def rules(self) -> Set[Specification]:
        return self.__rules

    @property
    def typeset(self) -> Typeset:
        return self.__typeset
