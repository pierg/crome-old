from enum import Enum, auto
from typing import Dict

from core.patterns import Pattern


class Robotic(Pattern):
    class Kinds(Enum):
        TRIGGER = auto()
        CORE_MOVEMENT = auto()

    patterns: Dict[Kinds, str] = {
        Kinds.TRIGGER: "TODO description...",
        Kinds.CORE_MOVEMENT: "TODO description...",
    }

    def __init__(self, formula: str, kind: Kinds):
        self.__formula: str = formula
        self.__kind: Robotic.Kinds = kind
        super().__init__(formula, Pattern.Kinds.ROBOTIC)
