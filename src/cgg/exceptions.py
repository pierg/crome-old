from __future__ import annotations
from typing import TYPE_CHECKING, Set

from goal.exceptions import GoalException

if TYPE_CHECKING:
    from cgg import Node

from enum import Enum


class CGGFailOperations(Enum):
    algebra_op = 0


class CGGFailMotivations(Enum):
    pass


class CGGException(Exception):
    def __init__(self, message: str):
        self.message = f"\n******CGG_EXCEPTION******\n{message}\n"
        print(self.message)


class CGGOperationFail(CGGException):
    def __init__(self, nodes: Set[Node], operation: CGGFailOperations, goal_ex: GoalException):
        self.nodes = nodes
        self.operation = operation
        self.goal_ex = goal_ex
        message = f"A failure has occurred while performing '{self.operation.name}' on nodes:\n" \
                  f"{', '.join(g.name for g in self.nodes)}"
        super().__init__(message=message)


class TransSynthesisFail(CGGException):
    def __init__(self, e):
        message = f"A failure has occurred while synthetizing the transition controllers\n{e}"
        super().__init__(message=message)
