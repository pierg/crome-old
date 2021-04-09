from typing import Union, Tuple

from specification import Specification
from specification.atom import Atom, AtomKind
from type import Boolean
from typeset import Typeset


class Pattern(Atom):
    """
    General LTL Pattern
    """

    def __init__(self,
                 formula: Tuple[str, Typeset] = None,
                 kind: AtomKind = None):
        if kind is None:
            kind = AtomKind.PATTERN
        super().__init__(
            formula=formula,
            kind=kind)


    @staticmethod
    def process_unary_input(element: Union[Specification, Boolean]) -> Tuple[str, Typeset]:

        typeset = Typeset()

        if isinstance(element, Boolean):
            input_str = element.name
            typeset |= element
        elif isinstance(element, Specification):
            input_str = element.string
            typeset |= element.typeset
        else:
            raise AttributeError

        return input_str, typeset

    @staticmethod
    def process_binary_input(pre: Union[Specification, Boolean], post: Union[Atom, Boolean]) -> Tuple[str, str, Typeset]:

        typeset = Typeset()

        if isinstance(pre, Boolean):
            pre_str = pre.name
            typeset |= pre
        elif isinstance(pre, Specification):
            pre_str = pre.string
            typeset |= pre.typeset
        else:
            raise AttributeError

        if isinstance(post, Boolean):
            post_str = post.name
            typeset |= post
        elif isinstance(post, Specification):
            post_str = post.string
            typeset |= post.typeset
        else:
            raise AttributeError

        return pre_str, post_str, typeset
