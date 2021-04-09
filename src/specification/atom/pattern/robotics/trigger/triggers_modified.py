from typing import Union
from specification.atom import Atom
from specification.atom.pattern.robotics.trigger import Trigger
from tools.logic import Logic
from type import Boolean


class InstantaneousReaction(Trigger):
    """Applies when the occurrence of a stimulus instantaneously triggers a counteraction."""

    def __init__(self, pre: Union[Atom, Boolean],
                 post: Union[Atom, Boolean],
                 context: Union[Atom, Boolean],
                 active: Union[Atom, Boolean]):
        new_typeset, pre, post, context, active = Trigger.process_bin_contextual_input(pre, post, context, active)

        c = Logic.and_([context, active])
        f = Logic.g_(Logic.implies_(Logic.and_([c, pre]), Logic.and_([c, post])))

        super().__init__(formula=(f, new_typeset))


class PromptReaction(Trigger):
    """Applies when the occurrence of a stimulus triggers a counteraction promptly, i.e. in the next time instant."""

    def __init__(self, pre: Union[Atom, Boolean],
                 post: Union[Atom, Boolean],
                 context: Union[Atom, Boolean],
                 active: Union[Atom, Boolean]):
        new_typeset, pre, post, context, active = Trigger.process_bin_contextual_input(pre, post, context, active)

        c = Logic.and_([context, active])
        f = Logic.g_(Logic.implies_(Logic.and_([c, pre]), Logic.and_([c, post])))

        super().__init__(formula=(f, new_typeset))


class DelayedReaction(Trigger):
    """Applies when the occurrence of a stimulus triggers a counteraction some time later."""

    def __init__(self, pre: Union[Atom, Boolean],
                 post: Union[Atom, Boolean],
                 context: Union[Atom, Boolean],
                 active: Union[Atom, Boolean]):
        new_typeset, pre, post, context, active = Trigger.process_bin_contextual_input(pre, post, context, active)

        c = Logic.and_([context, active])
        f = Logic.g_(Logic.implies_(Logic.and_([c, pre]), Logic.x_(Logic.w_(Logic.not_(c), Logic.and_([c, post])))))

        super().__init__(formula=(f, new_typeset))


class BoundReaction(Trigger):
    """Applies when a counteraction must be performed every time and only when a specific location is entered."""

    def __init__(self, pre: Union[Atom, Boolean],
                 post: Union[Atom, Boolean],
                 context: Union[Atom, Boolean],
                 active: Union[Atom, Boolean]):
        new_typeset, pre, post, context, active = Trigger.process_bin_contextual_input(pre, post, context, active)

        c = Logic.and_([context, active])
        f = Logic.g_(Logic.iff_(Logic.and_([c, pre]), Logic.and_([c, post])))

        super().__init__(formula=(f, new_typeset))


class BoundDelay(Trigger):
    """Applies when a counteraction must be performed every time and only when a specific location is entered."""

    def __init__(self, pre: Union[Atom, Boolean],
                 post: Union[Atom, Boolean],
                 context: Union[Atom, Boolean],
                 active: Union[Atom, Boolean]):
        new_typeset, pre, post, context, active = Trigger.process_bin_contextual_input(pre, post, context, active)

        c = Logic.and_([context, active])
        f = Logic.g_(Logic.iff_(Logic.and_([c, pre]), Logic.x_(Logic.w_(Logic.not_(c), Logic.and_([c, post])))))

        super().__init__(formula=(f, new_typeset))


class Wait(Trigger):
    """Applies when a counteraction must be performed every time and only when a specific location is entered..."""

    def __init__(self, pre: Union[Atom, Boolean],
                 post: Union[Atom, Boolean],
                 context: Union[Atom, Boolean],
                 active: Union[Atom, Boolean]):
        new_typeset, pre, post, context, active = Trigger.process_bin_contextual_input(pre, post, context, active)

        c = Logic.and_([context, active])
        f = Logic.u_(Logic.or_([Logic.and_([c, pre]),Logic.not_(c)]), Logic.and_([c, post]))
        super().__init__(formula=(f, new_typeset))


class GlobalAvoidance(Trigger):
    """Specifies that an avoidance condition globally holds."""

    def __init__(self, l: Union[Atom, Boolean]):
        new_typeset, l = Trigger.process_uni_input(l)

        f = Logic.g_(Logic.not_(l))

        super().__init__(formula=(f, new_typeset))
