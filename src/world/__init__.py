from specification.atom import Atom
from type.subtypes.active import Active
from typeset import Typeset

from typing import Set, TypeVar, Dict

from type import Types

AllTypes = TypeVar('AllTypes', bound=Types)


class World(Typeset):
    def __init__(self, types: Set[AllTypes] = None):
        types_with_active = types | {Active()}
        super().__init__(types_with_active)

    def get_atoms(self) -> Dict["str", Atom]:
        dictionary = {}
        for key, elem in self.items():
            dictionary[key] = elem.to_atom()

        return dictionary
