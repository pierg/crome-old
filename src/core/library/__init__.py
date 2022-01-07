from __future__ import annotations

from typing import Set

from core.cgg import Node
from core.goal import Goal


class Library:
    def __init__(self, goals: Set[Goal] = None):
        self.__goals = goals

    @property
    def goals(self):
        return self.__goals

    def add_goals(self, goals: Set[Goal]):
        self.__goals |= goals

    def search_refinement(self, goal_to_refine: Goal) -> Node | None:
        """Finds a composition of goals that refine 'goal_to_refine'."""

        for g in self.__goals:
            if g <= goal_to_refine:
                return Node(goal=g)

        return None
