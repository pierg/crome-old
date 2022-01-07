from typing import Set

from core.crometypes import Boolean, Types


class ReachLocation(Boolean):
    def __init__(self, name: str, mutex: str = None, adjacency: Set[str] = None):
        """adjacent_to is a set of strings where each string is the name of the
        class self is adjacent to."""
        super().__init__(name)

        if mutex is None:
            self.mutex = "locations"
        else:
            self.mutex = mutex

        if adjacency is None:
            self.adjacency = set()
        else:
            self.adjacency = adjacency

    def to_atom(self, kind=None):
        from core.specification import Specification

        return super().to_atom(kind=Specification.Kind.ATOM_LOCATION)

    @property
    def kind(self):
        return Types.Kind.LOCATION

    @property
    def adjacency_set(self) -> Set[str]:
        return self.adjacency

    @property
    def mutex_group(self):
        return self.mutex
