from __future__ import annotations

from typing import Set

from core.cgg import Node
from core.goal import Goal
from core.typeset import Typeset


class Library:
    def __init__(self, goals: Set[Goal] = None):
        self.__goals = goals
        self.__typeset = Typeset()
        for goal in goals:
            self.__typeset |= goal.specification.typeset

    @property
    def goals(self):
        return self.__goals

    def add_goals(self, goals: Set[Goal]):
        self.__goals |= goals
        for goal in goals:
            self.__typeset |= goal.specification.typeset

    def search_refinement(self, goal_to_refine: Goal) -> Node | None:
        """Finds a composition of goals that refine 'goal_to_refine'."""

        for g in self.__goals:
            if g <= goal_to_refine:
                return Node(goal=g)

        return None

    def covers(self, goal: Goal):
        """Return true if all the types of the goal are covered by the same
        type or refinements."""
        n_t_covered = 0
        for t_goal in goal.specification.typeset.values():
            t_covered = False
            for t_lib in self.__typeset.values():
                if t_lib <= t_goal:
                    t_covered = True
                    continue
            if not t_covered:
                return False
            else:
                n_t_covered += 1

        if n_t_covered == goal.specification.typeset.size():
            return True
        return False
