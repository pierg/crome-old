from abc import ABC
from enum import Enum, auto
from typing import Dict


class Pattern(ABC):
    class Kinds(Enum):
        ROBOTIC = auto()
        DWYER = auto()

    # TODO: to complete

    description: Dict[Kinds, str] = {
        Kinds.ROBOTIC: "TODO description...",
        Kinds.DWYER: "TODO description...",
    }

    def __init__(self, formula: str, kind: Kinds):
        self.__formula: str = formula
        self.__kind: Pattern.Kinds = kind

    def __str__(self):
        return self.__formula

    @property
    def formula(self) -> str:
        return self.__formula

    def kind(self) -> Kinds:
        return self.__kind
