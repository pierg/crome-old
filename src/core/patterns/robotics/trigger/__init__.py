from enum import Enum, auto
from typing import Dict

from core.patterns.robotics import Robotic
from tools.logic import Logic


class Trigger(Robotic):
    class Kinds(Enum):
        INSTANTANEOUS_REACTION = auto()
        BOUNDED_REACTION = auto()
        BOUND_DELAY = auto()
        DELAYED_REACTION = auto()
        WAIT = auto()

    patterns: Dict[Kinds, str] = {
        Kinds.INSTANTANEOUS_REACTION: "Applies when the occurrence of a stimulus instantaneously triggers a counteraction.",
        Kinds.BOUNDED_REACTION: "Applies when a counteraction must be performed every time and only when a specific location is entered.",
        Kinds.BOUND_DELAY: "Applies when a counteraction must be performed every time and only when a specific location is entered.",
        Kinds.PROMPT_REACTION: "Applies when the occurrence of a stimulus triggers a counteraction promptly, i.e. in the next time instant.",
        Kinds.DELAYED_REACTION: "Applies when the occurrence of a stimulus triggers a counteraction some time later.",
        Kinds.WAIT: "Applies when a counteraction must be performed every time and only when a specific location is entered.",
    }

    def __init__(self, formula: str, kind: Kinds):
        self.__formula: str = formula
        self.__kind: Trigger.Kinds = kind
        super().__init__(formula, Robotic.Kinds.TRIGGER)

    @staticmethod
    def check_inputs(pre: str, post: str):
        if not (isinstance(pre, str) and isinstance(post, str)):
            raise AttributeError


class InstantaneousReaction(Trigger):
    def __init__(self, pre: str, post: str):
        Trigger.check_inputs(pre, post)

        f = Logic.g_(Logic.implies_(pre, post))

        super().__init__(formula=f, kind=Trigger.Kinds.INSTANTANEOUS_REACTION)


class BoundReaction(Trigger):
    def __init__(self, pre: str, post: str):
        Trigger.check_inputs(pre, post)

        f = Logic.g_(Logic.iff_(pre, post))

        super().__init__(formula=f, kind=Trigger.Kinds.BOUNDED_REACTION)


class BoundDelay(Trigger):
    def __init__(self, pre: str, post: str):
        Trigger.check_inputs(pre, post)

        f = Logic.g_(Logic.iff_(pre, Logic.x_(post)))

        super().__init__(formula=f, kind=Trigger.Kinds.BOUND_DELAY)


class PromptReaction(Trigger):
    def __init__(self, pre: str, post: str):
        Trigger.check_inputs(pre, post)

        f = Logic.g_(Logic.implies_(pre, Logic.x_(post)))

        super().__init__(formula=f, kind=Trigger.Kinds.PROMPT_REACTION)


class DelayedReaction(Trigger):
    """Applies when the occurrence of a stimulus triggers a counteraction some
    time later."""

    def __init__(self, pre: str, post: str):
        Trigger.check_inputs(pre, post)

        f = Logic.g_(Logic.implies_(pre, Logic.f_(post)))

        super().__init__(formula=f, kind=Trigger.Kinds.DELAYED_REACTION)


class Wait(Trigger):
    def __init__(self, pre: str, post: str):
        Trigger.check_inputs(pre, post)

        f = Logic.u_(pre, post)

        super().__init__(formula=f, kind=Trigger.Kinds.WAIT)
