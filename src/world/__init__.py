from specification.atom import Atom
from type.subtypes.active import Active
from typeset import Typeset

from typing import Set, Dict

from type import Types


class World(Typeset):
    def __init__(self,
                 actions: Set[Types] = None,
                 locations: Set[Types] = None,
                 sensors: Set[Types] = None,
                 contexts: Set[Types] = None):
        types = actions | locations | sensors | contexts

        types_with_active = types | {Active()}

        super().__init__(types_with_active)

    def get_atoms(self) -> Dict[str, Atom]:
        dictionary = {}
        for key, elem in self.items():
            dictionary[key] = elem.to_atom()

        return dictionary
