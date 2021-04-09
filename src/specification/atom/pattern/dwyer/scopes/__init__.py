from formula.patterns.dywer import Pattern
from formula import LTL
from typeset import Typeset


class Scope(Pattern):

    def __init__(self, formula: str, variables: Typeset):
        super().__init__(formula=formula, variables=variables)


"""Scopes for the property 'P is true' defined by Dwyer"""


class P_global(Scope):
    """G p"""

    def __init__(self, p: LTL):
        formula = "G({p})".format(p=p.formula())
        super().__init__(formula, p.variables)


class P_before_R(Scope):
    """	F (r) -> (p U r) """

    def __init__(self, p: LTL, r: LTL):
        formula = "(F({r}) -> ({p} U {r}))".format(p=p.formula(), r=r.formula())
        super().__init__(formula, p.variables | r.variables)


class P_after_Q(Scope):
    """	G(q -> G(p)) """

    def __init__(self, p: LTL, q: LTL):
        formula = "(G({q} -> G({p})))".format(p=p.formula(), q=q.formula())
        super().__init__(formula, p.variables | q.variables)


class P_between_Q_and_R(Scope):
    """	G((q & !r & F r) -> (p U r)) """

    def __init__(self, p: LTL, q: LTL, r: LTL):
        formula = "(G(({q} & !{r} & F {r}) -> ({p} U {r})))".format(p=p.formula(), q=q.formula(), r=r.formula())
        super().__init__(formula, q.variables | r.variables)


class P_after_Q_until_R(Scope):
    """	G(q & !r -> ((p U r) | G p)) """

    def __init__(self, p: LTL, q: LTL, r: LTL):
        formula = "(G({q} & !{r} -> (({p} U {r}) | G {p})))".format(p=p.formula(), q=q.formula(), r=r.formula())
        super().__init__(formula, q.variables | r.variables)


"""Scopes for the property 'P becomes true' defined by Dwyer"""


class FP_global(Scope):
    """F p"""

    def __init__(self, p: LTL):
        formula = "F({p})".format(p=p.formula())
        super().__init__(formula, p.variables)


class FP_before_R(Scope):
    """	F (r) -> (!r U p) """

    def __init__(self, p: LTL, r: LTL):
        formula = "(F({r}) -> (!{r} U {p}))".format(p=p.formula(), r=r.formula())
        super().__init__(formula, p.variables | r.variables)


class FP_after_Q(Scope):
    """	G(!q) | F((q) & F (p)) """

    def __init__(self, p: LTL, q: LTL):
        formula = "(G(!{q}) | F(({q}) & F ({p})))".format(p=p.formula(), q=q.formula())
        super().__init__(formula, p.variables | q.variables)


class FP_between_Q_and_R(Scope):
    """	G((q & F(r)) -> (!(r) U (p))) """

    def __init__(self, p: LTL, q: LTL, r: LTL):
        formula = "(G(({q} & F({r})) -> (!({r}) U ({p}))))".format(p=p.formula(), q=q.formula(), r=r.formula())
        super().__init__(formula, p.variables | q.variables | r.variables)


class FP_after_Q_until_R(Scope):
    """	G((q) -> (!(r) U (p))) """

    def __init__(self, p: LTL, q: LTL, r: LTL):
        formula = "(G(({q}) -> (!({r}) U ({p}))))".format(p=p.formula(), q=q.formula(), r=r.formula())
        super().__init__(formula, p.variables | q.variables | r.variables)


"""Recurrence pattern"""


class Recurrence_P_between_Q_and_R(Scope):
    """TODO: Pattern as defined is always TRUE, TO BE FIXED"""
    """G((q & ! r & F r) -> ((F(p | r)) U r))"""

    def __init__(self, p: LTL, q: LTL, r: LTL):
        formula = "(G(({q} & ! {r} & F {r}) -> ((F({p} | {r})) U {r})))".format(p=p.formula(), q=q.formula(), r=r.formula())
        super().__init__(formula, p.variables | q.variables | r.variables)


class Recurrence_P_after_Q_until_R(Scope):
    """G((q & ! r) -> ((F(p | r)) U r))"""

    def __init__(self, p: LTL, q: LTL, r: LTL):
        formula = "(G(({q} & ! {r}) -> (((F({p} | {r})) U {r}) | G((F({p} | {r}))))))".format(p=p.formula(), q=q.formula(),
                                                                                              r=r.formula())
        super().__init__(formula, p.variables | q.variables | r.variables)


class Recurrence_P_after_Q_until_R_fixed(Scope):
    """G((q & ! r & F r) -> (F(p) U r))"""

    def __init__(self, p: LTL, q: LTL, r: LTL):
        formula = "(G(({q} & ! {r} & F {r}) -> (F({p}) U {r})))".format(p=p.formula(), q=q.formula(), r=r.formula())
        super().__init__(formula, p.variables | q.variables | r.variables)


"""Other dwyer defined"""


class P_until_R(Scope):
    """	(p U r) """

    def __init__(self, p: LTL, r: LTL):
        formula = "({p} U {r})".format(p=p.formula(), r=r.formula())
        super().__init__(formula, p.variables | r.variables)


class P_weakuntil_R(Scope):
    """	p W r = ((p U r) | G (p)) """

    def __init__(self, p: LTL, r: LTL):
        formula = "(({p} U {r}) | G ({p}))".format(p=p.formula(), r=r.formula())
        super().__init__(formula, p.variables | r.variables)


class P_release_R(Scope):
    """	p R r = !(!p U !r) """

    def __init__(self, p: LTL, r: LTL):
        formula = "!(!{p} U !{r})".format(r=r.formula(), p=p.formula())
        super().__init__(formula, p.variables | r.variables)


class P_strongrelease_R(Scope):
    """	p M r = ¬(¬p W ¬r) = r U (p & r) """

    def __init__(self, p: LTL, r: LTL):
        formula = "({r} U ({p} & {r}))".format(r=r.formula(), p=p.formula())
        super().__init__(formula, p.variables | r.variables)


"""Other pattern found"""


class P_exist_before_R(Scope):
    """	!r W (p & !r) = (!r U (p & !r)) | G (!r) """

    def __init__(self, p: LTL, r: LTL):
        formula = "((!{r} U ({p} & !{r})) | G (!{r}))".format(r=r.formula(), p=p.formula())
        super().__init__(formula, p.variables | r.variables)


class Absense_P_between_Q_and_R(Scope):
    """ G((q & !r & F r) -> (!p U r))"""

    def __init__(self, p: LTL, r: LTL, q: LTL):
        formula = "(G(({q} & !{r} & F {r}) -> (!{p} U {r})))".format(q=q.formula(), r=r.formula(), p=p.formula())
        super().__init__(formula, p.variables | q.variables | r.variables)


class Existence_P_between_Q_and_R(Scope):
    """ G(q & !r -> (!r W (p & !r))) = G(q & !r -> ((!r U (p & !r)) | G(!r)))"""

    def __init__(self, p: LTL, r: LTL, q: LTL):
        formula = "(G({q} & !{r} -> ((!{r} U ({p} & !{r})) | G(!{r}))))".format(q=q.formula(), r=r.formula(), p=p.formula())
        super().__init__(formula, p.variables | q.variables | r.variables)


class S_responds_to_P_before_R(Scope):
    """F r -> (p -> (!r U (s & !r))) U r"""

    def __init__(self, p: LTL, r: LTL, s: LTL):
        formula = "(F {r} -> ({p} -> (!{r} U ({s} & !{r}))) U {r})".format(s=s.formula(), r=r.formula(), p=p.formula())
        super().__init__(formula, p.variables | s.variables | r.variables)


class S_precedes_P(Scope):
    """!p W s = (!p U s) | G (!p) """

    def __init__(self, p: LTL, s: LTL):
        formula = "((!{p} U {s}) | G (!{p}))".format(s=s.formula(), p=p.formula())
        super().__init__(formula, p.variables | s.variables)
