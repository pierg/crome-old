from typing import Union
from specification.atom import Specification
from specification.atom.pattern import Pattern
from type import Boolean


class Init(Pattern):
    """Initial Position"""

    def __init__(self, element: Union[Specification, Boolean]):
        input_str, typeset = Pattern.process_unary_input(element)

        formula_str = f"{input_str}"

        super().__init__(
            formula=(formula_str, typeset))


class G(Pattern):
    """Globally"""

    def __init__(self, element: Union[Specification, Boolean]):
        input_str, typeset = Pattern.process_unary_input(element)

        formula_str = f"G({input_str})"

        super().__init__(
            formula=(formula_str, typeset))


class F(Pattern):
    """Eventually"""

    def __init__(self, element: Union[Specification, Boolean]):
        input_str, typeset = Pattern.process_unary_input(element)

        formula_str = f"F({input_str})"

        super().__init__(
            formula=(formula_str, typeset))


class X(Pattern):
    """Next"""

    def __init__(self, element: Union[Specification, Boolean]):
        input_str, typeset = Pattern.process_unary_input(element)

        formula_str = f"X({input_str})"

        super().__init__(
            formula=(formula_str, typeset))


class GF(Pattern):
    """Globally Eventually"""

    def __init__(self, element: Union[Specification, Boolean]):
        input_str, typeset = Pattern.process_unary_input(element)

        formula_str = f"G(F({input_str}))"

        super().__init__(
            formula=(formula_str, typeset))


class U(Pattern):
    """Until Pattern"""

    def __init__(self, pre: Union[Specification, Boolean], post: Union[Specification, Boolean]):
        pre_str, post_str, typeset = Pattern.process_binary_input(pre, post)

        formula_str = f"(({pre_str}) U ({post_str}))"

        super().__init__(
            formula=(formula_str, typeset))


class W(Pattern):
    """Weak Until Pattern"""

    def __init__(self, pre: Union[Specification, Boolean], post: Union[Specification, Boolean]):
        pre_str, post_str, typeset = Pattern.process_binary_input(pre, post)

        formula_str = f"((({pre_str}) U ({post_str})) | G({pre_str}))"

        super().__init__(
            formula=(formula_str, typeset))
