from __future__ import annotations

import itertools
from collections import Counter
from functools import reduce
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

    def get_candidate_composition(self, goal_to_refine: Goal):

        candidates = Counter()
        best_similar_types = 0

        for n in range(1, len(self.__goals)):
            for subset in itertools.combinations(self.__goals, n):
                n_compositions = len(subset)
                if n_compositions == 1:
                    subset_typeset = subset[0].specification.typeset
                else:
                    subset_typeset = reduce(
                        (lambda x, y: x | y), [g.specification.typeset for g in subset]
                    )
                similar_types = self.covers(goal_to_refine, subset_typeset)[1]
                if similar_types > best_similar_types:
                    composition = Node.composition(subset)
                    candidates = Counter()
                    best_similar_types = similar_types
                elif similar_types == best_similar_types:
                    composition = Node.composition(subset)
                    candidates[composition] = n_compositions

        print(
            f"There are {len(candidates.keys())} candidates with the same number of similar types: {best_similar_types}"
        )

        for node, count in candidates.items():
            print(f"{node.name}: {count}")

        # Filtering candidates with too many goals composed
        new_candidates = [
            x for x, count in candidates.items() if count == min(candidates.values())
        ]

        print("filtering...")
        print("\n".join(e.name for e in new_candidates))

        winner = self.get_most_refined(candidates)

        winner = self.get_most_refined(new_candidates)
        print(f"{winner.name} is the most refined candidate")
        return winner

    def get_most_refined(self, goals: list[Node]) -> Node:

        scores = Counter()

        for a, b in itertools.permutations(goals, 2):
            if a <= b:
                scores[a] += 1

        print("ratings")
        for node, count in scores.items():
            print(f"{node.name}: {count}")

        return scores.most_common(1)[0][0]

    def search_refinement(self, goal_to_refine: Goal) -> Node | None:
        """Finds a composition of goals that refine 'goal_to_refine'.

        MOCK UP OF GREEDY ALGORITHM IN COGOMO, TODO: integrate here
        """

        for n in range(1, len(self.__goals)):
            for subset in itertools.combinations(self.__goals, n):
                n_compositions = len(subset)
                if n_compositions == 1:
                    subset_typeset = subset[0].specification.typeset
                else:
                    subset_typeset = reduce(
                        (lambda x, y: x | y), [g.specification.typeset for g in subset]
                    )
                if not self.covers(goal_to_refine, subset_typeset)[0]:
                    continue
                g = Node.composition(subset)
                if g <= goal_to_refine:
                    return Node(goal=g)

        return None

    def covers(self, goal: Goal, typeset: Typeset = None) -> (bool, int):
        """Return true if all the types of the goal are covered by the same
        type or refinements.

        It also returns the number of similar types
        """
        if typeset is None:
            typeset = self.__typeset
        n_t_covered = 0
        for t_goal in goal.specification.typeset.values():
            t_covered = False
            for t_lib in typeset.values():
                if t_lib <= t_goal:
                    t_covered = True
                    continue
            if not t_covered:
                return False, n_t_covered
            else:
                n_t_covered += 1

        if n_t_covered == goal.specification.typeset.size():
            return True, n_t_covered
        return False, n_t_covered
