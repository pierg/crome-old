from enum import Enum, auto


class SpecKind(Enum):
    RULE = auto()
    ASSUMPTION = auto()
    GUARANTEE = auto()
    UNDEFINED = auto()


class AtomKind(Enum):
    SENSOR = auto()
    LOCATION = auto()
    ACTION = auto()
    TIME = auto()
    IDENTITY = auto()
    PATTERN = auto()
    ROBOTICPATTERN = auto()
    REFINEMENT_RULE = auto()
    ADJACENCY_RULE = auto()
    LIVENESS_RULE = auto()
    MUTEX_RULE = auto()
    UNDEFINED = auto()


class FormulaType(Enum):
    SATURATED = auto()
    UNSATURATED = auto()


class FormulaOutput(Enum):
    CNF = auto()
    DNF = auto()
    ListCNF = auto()


class FormulaKind(Enum):
    OBJECTIVE = auto()
    REFINEMENT_RULES = auto()
    MUTEX_RULES = auto()
    ADJACENCY_RULES = auto()
    UNDEFINED = auto()

