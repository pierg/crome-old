from typing import List, Union, Tuple
from specification.atom import Atom
from specification.atom.pattern.robotics import RoboticPattern
from type import Boolean
from typeset import Typeset


class Trigger(RoboticPattern):

    def __init__(self, formula: Tuple[str, Typeset] = None):
        super().__init__(formula=formula)

    @staticmethod
    def process_uni_input(l: Union[Atom, Boolean]) -> Tuple[Typeset, str]:

        new_typeset = Typeset()

        if isinstance(l, Boolean):
            new_typeset |= l
            l = l.name
        elif isinstance(l, Atom):
            new_typeset |= l.typeset
            l = l.string
        else:
            raise AttributeError

        return new_typeset, l

    @staticmethod
    def process_bin_input(pre: Union[Atom, Boolean], post: Union[Atom, Boolean]) -> Tuple[Typeset, str, str]:

        new_typeset = Typeset()

        if isinstance(pre, Boolean):
            new_typeset |= pre
            pre = pre.name
        elif isinstance(pre, Atom):
            new_typeset |= pre.typeset
            pre = pre.string
        else:
            raise AttributeError

        if isinstance(post, Boolean):
            new_typeset |= post
            post = post.name
        elif isinstance(post, Atom):
            new_typeset |= post.typeset
            post = post.string
        else:
            raise AttributeError

        return new_typeset, pre, post


    @staticmethod
    def process_bin_contextual_input(pre: Union[Atom, Boolean],
                                     post: Union[Atom, Boolean],
                                     context: Union[Atom, Boolean],
                                     active: Union[Atom, Boolean]) -> Tuple[Typeset, str, str, str, str]:

        new_typeset = Typeset()

        if isinstance(pre, Boolean):
            new_typeset |= pre
            pre = pre.name
        elif isinstance(pre, Atom):
            new_typeset |= pre.typeset
            pre = pre.string
        else:
            raise AttributeError

        if isinstance(post, Boolean):
            new_typeset |= post
            post = post.name
        elif isinstance(post, Atom):
            new_typeset |= post.typeset
            post = post.string
        else:
            raise AttributeError

        if isinstance(context, Boolean):
            new_typeset |= context
            context = context.name
        elif isinstance(context, Atom):
            new_typeset |= context.typeset
            context = context.string
        else:
            raise AttributeError

        if isinstance(active, Boolean):
            new_typeset |= active
            active = active.name
        elif isinstance(active, Atom):
            new_typeset |= active.typeset
            active = active.string
        else:
            raise AttributeError

        return new_typeset, pre, post, context, active
