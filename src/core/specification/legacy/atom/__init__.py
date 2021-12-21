from __future__ import annotations

from copy import deepcopy
from enum import Enum, auto
from typing import TYPE_CHECKING

from core.specification import Specification
from core.specification.enums import FormulaOutput, FormulaType, SpecKind
from core.specification.exceptions import AtomNotSatisfiableException
from core.type import Boolean, TypeKinds
from core.typeset import Typeset
from tools.logic import Logic, LogicTuple

if TYPE_CHECKING:
    from core.specification.legacy.formula import Formula


class Atom(Specification):
    class AtomKind(Enum):
        SENSOR = auto()
        LOCATION = auto()
        ACTION = auto()
        ACTIVE = auto()
        TIME = auto()
        CONTEXT = auto()
        IDENTITY = auto()
        PATTERN = auto()
        ROBOTICPATTERN = auto()
        REFINEMENT_RULE = auto()
        ADJACENCY_RULE = auto()
        LIVENESS_RULE = auto()
        MUTEX_RULE = auto()
        UNDEFINED = auto()

    def __init__(
        self,
        formula: str | tuple[str, Typeset] = None,
        kind: Atom.AtomKind = None,
        check: bool = True,
        dontcare: bool = False,
        typeset: Typeset = None,
    ):
        """Atomic Specification (can be an AP, but also an LTL_forced formula
        that cannot be broken down, e.g. a Pattern)"""

        if kind is None:
            self.__kind = AtomKind.UNDEFINED
        self.__kind = kind

        if (
            self.__kind == AtomKind.REFINEMENT_RULE
            or self.__kind == AtomKind.ADJACENCY_RULE
            or self.__kind == AtomKind.MUTEX_RULE
        ):
            self.__spec_kind = SpecKind.RULE
        else:
            self.__spec_kind = SpecKind.UNDEFINED

        # Indicates if the formula is negated
        self.__negation: bool = False

        # Indicates if the formula is a dontcare (weather is true or false)"""
        self.__dontcare: bool = dontcare

        # Used for linking guarantees to assumptions"""
        self.__saturation = None

        if formula is None:
            raise AttributeError
        if isinstance(formula, str):
            if formula == "TRUE":
                self.__base_formula: tuple[str, Typeset] = ("TRUE", Typeset())
            elif formula == "FALSE":
                self.__base_formula: tuple[str, Typeset] = ("FALSE", Typeset())
        else:
            self.__base_formula: tuple[str, Typeset] = formula

            if (
                check
                and kind != AtomKind.ADJACENCY_RULE
                and kind != AtomKind.MUTEX_RULE
                and kind != AtomKind.REFINEMENT_RULE
            ):
                if not self.is_satisfiable():
                    raise AtomNotSatisfiableException(
                        formula=self.__base_formula,
                    )

    def formula(self, type: FormulaType = FormulaType.SATURATED) -> (str, Typeset):
        expression, typeset = self.__base_formula
        if type == FormulaType.SATURATED:
            if self.__saturation is None:
                expression, typeset = self.__base_formula
            else:
                expression, typeset = LogicTuple.implies_(
                    prop_1=self.__saturation.formula(),
                    prop_2=self.__base_formula,
                    brackets=True,
                )
        if self.negated:
            return Logic.not_(expression), typeset
        return expression, typeset

    def negate(self):
        self.__negation = not self.negated

    def contains_rule(self, rule: AtomKind = None):
        if rule is None:
            return (
                self.kind == AtomKind.MUTEX_RULE
                or self.kind == AtomKind.REFINEMENT_RULE
                or self.kind == AtomKind.ADJACENCY_RULE
            )
        else:
            return self.kind == rule

    @property
    def unsaturated(self):
        return Atom(self.formula(FormulaType.UNSATURATED), self.kind)

    @property
    def kind(self) -> AtomKind:
        return self.__kind

    @kind.setter
    def kind(self, value: AtomKind):
        self.__kind = value

    @property
    def spec_kind(self) -> SpecKind:
        return self.__spec_kind

    @spec_kind.setter
    def spec_kind(self, value: SpecKind):
        self.__spec_kind = value

    @property
    def saturation(self):
        return self.__saturation

    def saturate(self, value: Specification):
        self.__saturation = value

    @property
    def negated(self) -> bool:
        return self.__negation

    @property
    def dontcare(self) -> bool:
        return self.__dontcare

    def get_dontcare(self) -> Atom:
        """Returns a new Atom which is a don't care of self."""
        new_formula = deepcopy(self)
        new_formula.__dontcare = True
        return new_formula

    def __hash__(self):
        return hash(self.__base_formula[0])

    def __and__(self, other: Atom | Formula) -> Formula:
        """self & other Returns a new Specification with the conjunction with
        other."""
        from core.specification.legacy.formula import Formula

        if isinstance(other, Atom):
            other = Formula(atom=other)

        return Formula(atom=self) & other

    def __or__(self, other: Atom | Formula) -> Formula:
        """self | other Returns a new Specification with the disjunction with
        other."""
        from core.specification.legacy.formula import Formula

        if isinstance(other, Atom):
            other = Formula(atom=other)

        return Formula(atom=self) | other

    def __invert__(self) -> Atom:
        """Returns a new Specification with the negation of self."""
        new_formula = deepcopy(self)
        new_formula.__negation = not new_formula.__negation
        return new_formula

    def __rshift__(self, other: Atom | Formula) -> Formula:
        """>> Returns a new Specification that is the result of self -> other
        (implies)"""
        from core.specification.legacy.formula import Formula

        if not (isinstance(other, Atom) or isinstance(other, Formula)):
            raise AttributeError
        if isinstance(other, Atom):
            other = Formula(atom=other)

        return Formula(atom=self) >> other

    def __lshift__(self, other: Atom | Formula) -> Formula:
        """<< Returns a new Specification that is the result of other -> self
        (implies)"""
        from core.specification.legacy.formula import Formula

        if not (isinstance(other, Atom) or isinstance(other, Formula)):
            raise AttributeError
        if isinstance(other, Atom):
            other = Formula(atom=other)

        return Formula(atom=self) << other

    def __iand__(self, other: Atom | Formula) -> Formula:
        """self &= other Produces a Formula which is the conjunction of self
        with other."""

        return self & other

    def __ior__(self, other: Atom | Formula) -> Formula:
        """self |= other Produces a Formula which is the disjunction of self
        with other."""

        return self | other

    @staticmethod
    def extract_refinement_rules(
        typeset: Typeset,
        output=None,
    ) -> Atom | tuple[list[str], Typeset] | None:
        """Extract Refinement rules from the Formula."""

        rules_str = []
        rules_typeset = Typeset()

        for key_type, set_super_types in typeset.super_types.items():
            if isinstance(key_type, Boolean):
                for super_type in set_super_types:
                    rules_str.append(
                        Logic.g_(
                            Logic.implies_(
                                key_type.name,
                                super_type.name,
                            ),
                        ),
                    )
                    rules_typeset |= Typeset({key_type})
                    rules_typeset |= Typeset(set_super_types)

        if len(rules_str) == 0:
            return None

        if output is not None and output == FormulaOutput.ListCNF:
            return rules_str, rules_typeset

        return Atom(
            formula=(Logic.and_(rules_str, brackets=True), rules_typeset),
            kind=AtomKind.MUTEX_RULE,
        )

    @staticmethod
    def extract_mutex_rules(
        typeset: Typeset,
        output=None,
    ) -> Atom | tuple[list[str], Typeset]:
        """Extract Mutex rules from the Formula."""

        rules_str = []
        rules_typeset = Typeset()

        for mutex_group in typeset.mutex_types:
            or_elements = []
            if len(mutex_group) > 1:
                for mutex_type in mutex_group:
                    neg_group = mutex_group.symmetric_difference({mutex_type})
                    and_elements = [mutex_type.name]
                    for elem in neg_group:
                        and_elements.append(Logic.not_(elem.name))
                    or_elements.append(Logic.and_(and_elements, brackets=True))
                rules_str.append(
                    Logic.g_(Logic.or_(or_elements, brackets=False)),
                )
                rules_typeset |= Typeset(mutex_group)

        if len(rules_str) == 0:
            return Atom("TRUE")

        if output is not None and output == FormulaOutput.ListCNF:
            return rules_str, rules_typeset

        return Atom(
            formula=(Logic.and_(rules_str, brackets=True), rules_typeset),
            kind=AtomKind.MUTEX_RULE,
        )

    @staticmethod
    def extract_adjacency_rules(
        typeset: Typeset,
        output=None,
    ) -> Atom | tuple[list[str], Typeset] | None:
        """Extract Adjacency rules from the Formula."""

        rules_str = []
        rules_typeset = Typeset()

        for key_type, set_adjacent_types in typeset.adjacent_types.items():
            if isinstance(key_type, Boolean):
                # G(a -> X(b | c | d))
                rules_str.append(
                    Logic.g_(
                        Logic.implies_(
                            key_type.name,
                            Logic.x_(
                                Logic.or_(
                                    [e.name for e in set_adjacent_types],
                                ),
                            ),
                        ),
                    ),
                )
                rules_typeset |= Typeset({key_type})
                rules_typeset |= Typeset(set_adjacent_types)

        if len(rules_str) == 0:
            return None

        if output is not None and output == FormulaOutput.ListCNF:
            return rules_str, rules_typeset

        return Atom(
            formula=(Logic.and_(rules_str, brackets=True), rules_typeset),
            kind=AtomKind.ADJACENCY_RULE,
        )

    @staticmethod
    def extract_liveness_rules(
        typeset: Typeset,
        output=None,
    ) -> Atom | tuple[list[str], Typeset] | None:
        """Extract Liveness rules from the Formula."""

        rules_str = []
        rules_typeset = Typeset()

        sensors, outs = typeset.extract_inputs_outputs()

        for t in sensors:
            if isinstance(t, Boolean):
                if t.kind == TypeKinds.SENSOR:
                    rules_str.append(Logic.g_(Logic.f_(t.name)))
                rules_typeset |= Typeset({t})

        if len(rules_str) == 0:
            return None

        if output is not None and output == FormulaOutput.ListCNF:
            return rules_str, rules_typeset

        return Atom(
            formula=(Logic.and_(rules_str, brackets=True), rules_typeset),
            kind=AtomKind.LIVENESS_RULE,
        )

    @staticmethod
    def context_active_rules(
        typeset: Typeset,
        output=None,
    ) -> Atom | tuple[list[str], Typeset] | None:
        """Extract Liveness rules from the Formula."""

        rules_str = []
        rules_typeset = Typeset()

        inputs, outs = typeset.extract_inputs_outputs()

        active_context_types = []
        for t in inputs:
            if isinstance(t, Boolean):
                if t.kind == TypeKinds.ACTIVE or t.kind == TypeKinds.CONTEXT:
                    active_context_types.append(t.name)
                rules_typeset |= Typeset({t})

        if len(active_context_types) > 0:
            rules_str.append(Logic.g_(Logic.and_(active_context_types)))

        if len(rules_str) == 0:
            return None

        if output is not None and output == FormulaOutput.ListCNF:
            return rules_str, rules_typeset

        return Atom(
            formula=(Logic.and_(rules_str, brackets=True), rules_typeset),
            kind=AtomKind.LIVENESS_RULE,
        )