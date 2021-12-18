from __future__ import annotations

import itertools
from copy import deepcopy
from typing import TYPE_CHECKING

from core.specification import Specification
from core.specification.enums import FormulaKind, FormulaOutput, SpecKind
from core.specification.exceptions import NotSatisfiableException
from core.typeset import Typeset
from tools.logic import Logic, LogicTuple
from tools.nuxmv import Nuxmv

if TYPE_CHECKING:
    from core.specification.legacy.atom import Atom, AtomKind


class Formula(Specification):
    def __init__(
        self,
        atom: Atom | str = None,
        kind: FormulaKind = None,
    ):

        if kind is None:
            self.__kind = FormulaKind.UNDEFINED
        self.__kind = kind

        if (
            self.__kind == FormulaKind.REFINEMENT_RULES
            or self.__kind == FormulaKind.ADJACENCY_RULES
            or self.__kind == FormulaKind.MUTEX_RULES
        ):
            self.__spec_kind = SpecKind.RULE
        else:
            self.__spec_kind = SpecKind.UNDEFINED

        if isinstance(atom, str) and atom == "TRUE":
            from core.specification.legacy.atom import Atom

            new_atom = Atom("TRUE")
            self.__cnf: list[set[Atom]] = [{new_atom}]
            self.__dnf: list[set[Atom]] = [{new_atom}]

        elif isinstance(atom, str) and atom == "FALSE":
            from core.specification.legacy.atom import Atom

            new_atom = Atom("FALSE")
            self.__cnf: list[set[Atom]] = [{new_atom}]
            self.__dnf: list[set[Atom]] = [{new_atom}]

        elif atom is not None:
            self.__cnf: list[set[Atom]] = [{atom}]
            self.__dnf: list[set[Atom]] = [{atom}]

        else:
            raise Exception("Wrong parameters LTL_forced construction")

    @property
    def kind(self) -> FormulaKind:
        return self.__kind

    @kind.setter
    def kind(self, value: FormulaKind):
        self.__kind = value

    @property
    def spec_kind(self) -> SpecKind:
        return self.__spec_kind

    @spec_kind.setter
    def spec_kind(self, value: SpecKind):
        self.__spec_kind = value

    @property
    def cnf(self) -> list[set[Atom]]:
        return self.__cnf

    @property
    def dnf(self) -> list[set[Atom]]:
        return self.__dnf

    def _remove_atoms(self, atoms_to_remove: set[Atom]):
        """Remove Atoms from Formula."""

        if len(atoms_to_remove) == 1 and list(atoms_to_remove)[0].is_true():
            return

        """Remove from CNF"""
        for clause in self.__dnf:
            clause -= atoms_to_remove

        """Remove from CNF"""
        clause_cnf_to_remove = set()
        for clause in self.__cnf:
            """Remove clause if contains atoms to be removed."""
            if clause & atoms_to_remove:
                clause_cnf_to_remove |= clause

        """Filter out clauses"""
        for clause in list(self.cnf):
            if len(clause & clause_cnf_to_remove) > 0:
                self.__cnf.remove(clause)

        if len(self.atoms) == 0:
            new_atom = Atom("TRUE")
            self.__cnf: list[set[Atom]] = [{new_atom}]
            self.__dnf: list[set[Atom]] = [{new_atom}]

    def relax_by(self, formula: Formula):
        """Given the assumption as set of conjunctive clauses connected by the
        disjunction operator (DNF), we can simplify any conjunct a_i in a
        clause x if exists a guarantee (a_j -> g_j) such that: 1) a_j is part
        of x 2) g_j -> a_i is a valid formula.

        DNF = (a & b) | (c & d)
        CNF = (a | c) & (a | d) & (b | c) & (b | d)

        simplify a =>
        DNF = (b) | (c & d)
        CNF = (b | c) & (b | d)
        """
        for guarantee in formula.cnf:
            if len(guarantee) == 1:
                g = list(guarantee)[0]
            else:
                # TODO: Change
                continue
            atoms_to_remove = set()
            for clause in self.dnf:
                if g.saturation is not None:
                    if g.saturation in clause:
                        for conjunct in clause:
                            if not conjunct.is_true():
                                if (g.unsaturated >> conjunct).is_valid():
                                    print(f"{str(g)} relaxes {str(conjunct)}")
                                    atoms_to_remove.add(conjunct)
                else:
                    for conjunct in clause:
                        if not conjunct.is_true():
                            if (g.unsaturated >> conjunct).is_valid():
                                print(f"{str(g)} relaxes {str(conjunct)}")
                                atoms_to_remove.add(conjunct)

            self._remove_atoms(atoms_to_remove)

    @property
    def atoms(self) -> set[Atom]:
        new_set = set()
        for group in self.cnf:
            new_set |= group
        return new_set

    def contains_rule(self, rule: AtomKind = None):
        return any([e.contains_rule(rule) for e in self.atoms])

    def saturate(self, value: Specification):
        """Saturate each atom of the formula, CNF and DNF x->((a | b) & (c |
        d)) === ((x->a) | (x->b)) & ((x->c) | (x->d)) x->((a & b) | (c & d))

        === ((x->a) & (x->b)) | ((x->c) & (x->d))
        """
        # if not value.is_true():
        for clause in self.cnf:
            for atom in clause:
                atom.saturate(value)
        """Atoms are shared between CNF and DNF"""

    def formula(
        self,
        formulatype: FormulaOutput = FormulaOutput.CNF,
    ) -> (tuple[str, Typeset] | tuple[list[str], Typeset]):
        """Generate the formula."""

        if formulatype == FormulaOutput.CNF:
            return LogicTuple.and_(
                [
                    LogicTuple.or_(
                        [atom.formula() for atom in clause],
                        brakets=True,
                    )
                    for clause in self.cnf
                ],
                brackets=False,
            )

        if formulatype == FormulaOutput.ListCNF:
            return [
                Logic.or_([atom.string for atom in clause]) for clause in self.cnf
            ], self.typeset

        if formulatype == FormulaOutput.DNF:
            return LogicTuple.or_(
                [
                    LogicTuple.and_(
                        [atom.formula() for atom in clause],
                        brackets=True,
                    )
                    for clause in self.dnf
                ],
                brakets=False,
            )

    @staticmethod
    def satcheck(formulas: set[Formula]) -> bool:
        print("\t\tSATCHECK")
        for f in formulas:
            if f.is_false():
                return False
        f_typeset = Typeset()
        f_string = []

        for f in formulas:
            f_typeset |= f.typeset
            f_string.append(f.string)

        formula_check = Logic.and_(f_string)

        from core.specification.legacy.atom import Atom

        rules = Atom.extract_mutex_rules(f_typeset)
        if rules is not None:
            Logic.and_([formula_check, rules.string])
            f_typeset |= rules.typeset

        return Nuxmv.check_satisfiability((formula_check, f_typeset))

    def __and__(self, other: Formula | Atom) -> Formula:
        """self & other Returns a new Specification with the conjunction with
        other."""
        new_ltl = deepcopy(self)
        new_ltl &= other
        return new_ltl

    def __or__(self, other: Formula | Atom) -> Formula:
        """self | other Returns a new Specification with the disjunction with
        other."""
        new_ltl = deepcopy(self)
        new_ltl |= other
        return new_ltl

    def __invert__(self) -> Formula:
        """Returns a new Specification with the negation of self."""

        new_ltl = deepcopy(self)

        """Negate all atoms"""
        for atom in new_ltl.atoms:
            atom.negate()

        """Swap CNF with DNF"""
        new_ltl.__cnf, new_ltl.__dnf = new_ltl.dnf, new_ltl.cnf

        return new_ltl

    def __rshift__(self, other: Formula | Atom) -> Formula:
        """>> Returns a new Specification that is the result of self -> other
        (implies) NOT self OR other."""
        from core.specification.legacy.atom import Atom

        if isinstance(other, Atom):
            other = Formula(other)

        if self.is_true():
            return other

        new_ltl = ~self

        return new_ltl | other

    def __lshift__(self, other: Formula | Atom) -> Formula:
        """<< Returns a new Specification that is the result of other -> self
        (implies) NOT other OR self."""
        from core.specification.legacy.atom import Atom

        if isinstance(other, Atom):
            other = Formula(other)

        new_ltl = ~other

        return new_ltl | self

    def __iand__(self, other: Formula | Atom) -> Formula:
        """self &= other Modifies self with the conjunction with other."""
        from core.specification.legacy.atom import Atom

        """Base cases"""
        if isinstance(other, Atom):
            other = Formula(other)

        if other.is_false():
            new_atom = Atom("FALSE")
            self.__cnf: list[set[Atom]] = [{new_atom}]
            self.__dnf: list[set[Atom]] = [{new_atom}]
            return self

        if other.is_true():
            return self

        if self.is_false():
            self.__cnf = other.cnf
            self.__dnf = other.dnf
            return self

        if self.is_true():
            new_other = deepcopy(other)
            self.__cnf: list[set[Atom]] = new_other.cnf
            self.__dnf: list[set[Atom]] = new_other.dnf
            return self

        new_other = deepcopy(other)
        new_self = deepcopy(self)

        """Mutex Rules necessary for Satisfiability Check"""
        rules = Atom.extract_mutex_rules(self.typeset | other.typeset)

        """Cartesian product between the two dnf"""
        temp_dnf = []
        for a, b in itertools.product(self.dnf, new_other.dnf):

            new_set = a | b

            check_formula = LogicTuple.and_([f.formula() for f in new_set])

            atom = Atom(formula=check_formula, check=False)

            if atom.is_satisfiable():
                temp_dnf.append(new_set)

        if len(temp_dnf) == 0:
            raise NotSatisfiableException(self, other, rules)
        else:
            self.__dnf = temp_dnf

        redundant_index = set()
        """Append to list if not already there"""
        for s_i, self_clause in enumerate(new_self.cnf):
            self_s, self_t = LogicTuple.or_(
                [atom.formula() for atom in self_clause],
            )
            self_atom = Atom(formula=(self_s, self_t), check=False)
            """check if another clause is already a refinement of the existing one"""

            for o_i, other_clause in enumerate(other.cnf):
                if o_i in redundant_index:
                    continue
                other_s, other_t = LogicTuple.or_(
                    [atom.formula() for atom in other_clause],
                )
                other_atom = Atom(formula=(other_s, other_t), check=False)

                if self_atom <= other_atom:
                    """If an existing clause is already a refinement then skip
                    it."""
                    redundant_index.add(o_i)
                    break
                if other_atom <= self_atom:
                    """If the other is a refinement, then substitute it."""
                    self.__cnf[s_i] = other_clause
                    redundant_index.add(o_i)
                    break

                """Otherwise append it"""
                self.__cnf.append(other_clause)

        return self

    def __ior__(self, other: Formula | Atom) -> Formula:
        """self }= other Modifies self with the disjunction with other."""
        from core.specification.legacy.atom import Atom

        """Base cases"""
        if isinstance(other, Atom):
            other = Formula(other)

        if other.is_false():
            return self

        if other.is_true():
            new_atom = Atom("TRUE")
            self.__cnf: list[set[Atom]] = [{new_atom}]
            self.__dnf: list[set[Atom]] = [{new_atom}]
            return self

        if self.is_true():
            return self

        if self.is_false():
            new_other = deepcopy(other)
            self.__cnf: list[set[Atom]] = new_other.cnf
            self.__dnf: list[set[Atom]] = new_other.dnf
            return self

        new_other = deepcopy(other)
        new_self = deepcopy(self)

        """Cartesian product between the two cnf"""
        temp_cnf = []
        for a, b in itertools.product(self.cnf, new_other.cnf):

            new_set = a | b

            check_formula = LogicTuple.or_([f.formula() for f in new_set])

            atom = Atom(formula=check_formula, check=False)

            if not atom.is_valid():
                temp_cnf.append(new_set)

        if len(temp_cnf) == 0:
            new_atom = Atom("TRUE")
            self.__cnf: list[set[Atom]] = [{new_atom}]
            self.__dnf: list[set[Atom]] = [{new_atom}]
            return self
        else:
            self.__cnf = temp_cnf

        redundant_index = set()
        """Append to list if not already there"""
        for s_i, self_clause in enumerate(new_self.dnf):
            self_s, self_t = LogicTuple.and_(
                [atom.formula() for atom in self_clause],
            )
            self_atom = Atom(formula=(self_s, self_t), check=False)
            """check if another clause is already a refinement of the existing one"""

            for o_i, other_clause in enumerate(other.dnf):
                if o_i in redundant_index:
                    continue
                other_s, other_t = LogicTuple.and_(
                    [atom.formula() for atom in other_clause],
                )
                other_atom = Atom(formula=(other_s, other_t), check=False)

                if other_atom <= self_atom:
                    """If an other clause is a refinement then skip it."""
                    redundant_index.add(o_i)
                    break
                if self_atom <= other_atom:
                    """If existing clause is a refinement, then substitute
                    it."""
                    self.__dnf[s_i] = other_clause
                    redundant_index.add(o_i)
                    break

                """Otherwise append it"""
                self.__dnf.append(other_clause)

        return self
