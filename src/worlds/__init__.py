from typeset import Typeset

from typing import Set, TypeVar

from type import Types

AllTypes = TypeVar('AllTypes', bound=Types)


class World(Typeset):
    def __init__(self, types: Set[AllTypes] = None):
        super().__init__(types)
