from __future__ import annotations
from typing import TYPE_CHECKING, Set

from contract import ContractException
from controller.exceptions import ControllerException

if TYPE_CHECKING:
    from goal import Goal

from enum import Enum


class GoalFailOperations(Enum):
    composition = 0
    conjunction = 1
    refinement = 2
    synthesis = 3


class GoalFailMotivations(Enum):
    goal_not_found = 0
    inconsistent = 1
    incompatible = 2
    unfeasible = 3
    wrong_refinement = 4


class GoalException(Exception):
    def __init__(self, message: str):
        self.message = f"\n******GOAL_EXCEPTION******\n{message}\n"
        print(self.message)


class GoalAlgebraOperationFail(GoalException):
    def __init__(self, goals: Set[Goal], operation: GoalFailOperations, contr_ex: ContractException):
        self.goals = goals
        self.operation = operation
        self.contr_ex = contr_ex
        message = f"A failure has occurred while performing '{self.operation.name}' on goals:\n" \
                  f"{', '.join(g.name for g in self.goals)}"
        super().__init__(message=message)


class GoalSynthesisFail(GoalException):
    def __init__(self, goal: Goal, controller_ex: ControllerException):
        self.goal = goal
        self.controller_ex = controller_ex
        message = f"A failure has occurred while performing trying to realize the goal '{goal.name}'"
        super().__init__(message=message)

