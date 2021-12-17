from enum import Enum, auto
from typing import Dict

from core.patterns.robotics import Robotic


class CoreMovement(Robotic):
    class Kinds(Enum):
        COVERAGE = auto()
        SURVEILLANCE = auto()

    patterns: Dict[Kinds, str] = {
        Kinds.COVERAGE: "TODO description...",
        Kinds.SURVEILLANCE: "TODO description...",
    }

    def __init__(self, formula: str, kind: Kinds):
        self.__formula: str = formula
        self.__kind: CoreMovement.Kinds = kind
        super().__init__(formula, Robotic.Kinds.CORE_MOVEMENT)
