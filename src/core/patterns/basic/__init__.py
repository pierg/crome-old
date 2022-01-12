from core.patterns import Pattern


class Init(Pattern):
    """Initial Position."""

    def __init__(self, element: str):
        Pattern.process_unary_input(element)

        formula = f"{element}"

        super().__init__(formula, Pattern.Kinds.BASIC)


class G(Pattern):
    """Globally."""

    def __init__(self, element: str):
        Pattern.process_unary_input(element)

        formula = f"G({element})"

        super().__init__(formula, Pattern.Kinds.BASIC)


class F(Pattern):
    """Eventually."""

    def __init__(self, element: str):
        Pattern.process_unary_input(element)

        formula = f"F({element})"

        super().__init__(formula, Pattern.Kinds.BASIC)


class X(Pattern):
    """Next."""

    def __init__(self, element: str):
        Pattern.process_unary_input(element)

        formula = f"X({element})"

        super().__init__(formula, Pattern.Kinds.BASIC)


class GF(Pattern):
    """Globally Eventually."""

    def __init__(self, element: str):
        Pattern.process_unary_input(element)

        formula = f"G(F({element}))"

        super().__init__(formula, Pattern.Kinds.BASIC)


class U(Pattern):
    """Until Pattern."""

    def __init__(self, pre: str, post: str):
        Pattern.process_binary_input(pre, post)

        formula = f"(({pre}) U ({post}))"

        super().__init__(formula, Pattern.Kinds.BASIC)


class W(Pattern):
    """Weak Until Pattern."""

    def __init__(self, pre: str, post: str):
        Pattern.process_binary_input(pre, post)

        formula = f"((({pre}) U ({post})) | G({pre}))"

        super().__init__(formula, Pattern.Kinds.BASIC)
