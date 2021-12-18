from typing import Union

from core.specification import Specification
from core.specification.legacy.formula import Trigger
from core.type import Boolean
from tools.logic import Logic


class InstantaneousReaction(Trigger):
    """Applies when the occurrence of a stimulus instantaneously triggers a
    counteraction."""

    def __init__(
        self, pre: Union[Specification, Boolean], post: Union[Specification, Boolean]
    ):
        new_typeset, pre, post = Trigger.process_bin_input(pre, post)

        f = Logic.g_(Logic.implies_(pre, post))

        super().__init__(formula=(f, new_typeset))


class BoundReaction(Trigger):
    """Applies when a counteraction must be performed every time and only when
    a specific location is entered."""

    def __init__(
        self, pre: Union[Specification, Boolean], post: Union[Specification, Boolean]
    ):
        new_typeset, pre, post = Trigger.process_bin_input(pre, post)

        f = Logic.g_(Logic.iff_(pre, post))

        super().__init__(formula=(f, new_typeset))


class BoundDelay(Trigger):
    """Applies when a counteraction must be performed every time and only when
    a specific location is entered."""

    def __init__(
        self, pre: Union[Specification, Boolean], post: Union[Specification, Boolean]
    ):
        new_typeset, pre, post = Trigger.process_bin_input(pre, post)

        f = Logic.g_(Logic.iff_(pre, Logic.x_(post)))

        super().__init__(formula=(f, new_typeset))


class PromptReaction(Trigger):
    """Applies when the occurrence of a stimulus triggers a counteraction
    promptly, i.e. in the next time instant."""

    def __init__(
        self, pre: Union[Specification, Boolean], post: Union[Specification, Boolean]
    ):
        new_typeset, pre, post = Trigger.process_bin_input(pre, post)

        f = Logic.g_(Logic.implies_(pre, Logic.x_(post)))

        super().__init__(formula=(f, new_typeset))


class DelayedReaction(Trigger):
    """Applies when the occurrence of a stimulus triggers a counteraction some
    time later."""

    def __init__(
        self, pre: Union[Specification, Boolean], post: Union[Specification, Boolean]
    ):
        new_typeset, pre, post = Trigger.process_bin_input(pre, post)

        f = Logic.g_(Logic.implies_(pre, Logic.f_(post)))

        super().__init__(formula=(f, new_typeset))


class Wait(Trigger):
    """Applies when a counteraction must be performed every time and only when
    a specific location is entered..."""

    def __init__(
        self, pre: Union[Specification, Boolean], post: Union[Specification, Boolean]
    ):
        new_typeset, pre, post = Trigger.process_bin_input(pre, post)

        f = Logic.u_(pre, post)

        super().__init__(formula=(f, new_typeset))


class ConditionalWait(Trigger):
    """Applies when a counteraction must be performed every time and only when
    a specific location is entered..."""

    def __init__(
        self, pre: Union[Specification, Boolean], post: Union[Specification, Boolean]
    ):
        new_typeset, pre, post = Trigger.process_bin_input(pre, post)

        f = Logic.g_(Logic.implies_(pre, Logic.u_(pre, post)))

        super().__init__(formula=(f, new_typeset))


class GlobalAvoidance(Trigger):
    """Specifies that an avoidance condition globally holds."""

    def __init__(self, l: Union[Specification, Boolean]):
        new_typeset, l = Trigger.process_uni_input(l)

        f = Logic.g_(Logic.not_(l))

        super().__init__(formula=(f, new_typeset))
