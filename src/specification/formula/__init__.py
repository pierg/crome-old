from __future__ import annotations

import itertools
from copy import deepcopy, copy
from enum import Enum, auto
from typing import Set, Tuple, TYPE_CHECKING, List, Union

from specification import Specification
from specification.enums import *
from specification.exceptions import NotSatisfiableException, AtomNotSatisfiableException
from tools.logic import LogicTuple, Logic
from tools.nuxmv import Nuxmv
from type import Boolean
from typeset import Typeset

if TYPE_CHECKING:
    from specification.atom import Atom, AtomKind


class Formula(Specification):
    def __init__(self,
                 atom: Union[Atom, str] = None,
                 kind: FormulaKind = None):

        if kind is None:
            self.__kind = FormulaKind.UNDEFINED
        self.__kind = kind

        if self.__kind == FormulaKind.REFINEMENT_RULES or \
                self.__kind == FormulaKind.ADJACENCY_RULES or \
                self.__kind == FormulaKind.MUTEX_RULES:
            self.__spec_kind = SpecKind.RULE
        else:
            self.__spec_kind = SpecKind.UNDEFINED

        if isinstance(atom, str) and atom == "TRUE":
            from specification.atom import Atom
            new_atom = Atom("TRUE")
            self.__cnf: List[Set[Atom]] = [{new_atom}]
            self.__dnf: List[Set[Atom]] = [{new_atom}]

        elif isinstance(atom, str) and atom == "FALSE":
            from specification.atom import Atom
            new_atom = Atom("FALSE")
            self.__cnf: List[Set[Atom]] = [{new_atom}]
            self.__dnf: List[Set[Atom]] = [{new_atom}]

        elif atom is not None:
            self.__cnf: List[Set[Atom]] = [{atom}]
            self.__dnf: List[Set[Atom]] = [{atom}]

        else:
            raise Exception("Wrong parameters LTL construction")

    from ._printing import pretty_print

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
    def cnf(self) -> List[Set[Atom]]:
        return self.__cnf

    @property
    def dnf(self) -> List[Set[Atom]]:
        return self.__dnf

    def _remove_atoms(self, atoms_to_remove: Set[Atom]):
        """Remove Atoms from Formula"""

        if len(atoms_to_remove) == 1 and list(atoms_to_remove)[0].is_true():
            return

        """Remove from CNF"""
        for clause in self.__dnf:
            clause -= atoms_to_remove

        """Remove from CNF"""
        clause_cnf_to_remove = set()
        for clause in self.__cnf:
            """Remove clause if contains atoms to be removed"""
            if clause & atoms_to_remove:
                clause_cnf_to_remove |= clause

        """Filter out clauses"""
        for clause in list(self.cnf):
            if len(clause & clause_cnf_to_remove) > 0:
                self.__cnf.remove(clause)

        if len(self.atoms) == 0:
            new_atom = Atom("TRUE")
            self.__cnf: List[Set[Atom]] = [{new_atom}]
            self.__dnf: List[Set[Atom]] = [{new_atom}]

    def relax_by(self, formula: Formula):
        """
        Given the assumption as set of conjunctive clauses connected by the disjunction operator (DNF),
        we can simplify any conjunct a_i in a clause x if exists a guarantee (a_j -> g_j) such that:
        1) a_j is part of x
        2) g_j -> a_i is a valid formula

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
    def atoms(self) -> Set[Atom]:
        new_set = set()
        for group in self.cnf:
            new_set |= group
        return new_set

    def contains_rule(self, rule: AtomKind = None):
        return any([e.contains_rule(rule) for e in self.atoms])

    def saturate(self, value: Specification):
        """
        Saturate each atom of the formula, CNF and DNF
        x->((a | b) & (c | d)) === ((x->a) | (x->b)) & ((x->c) | (x->d))
        x->((a & b) | (c & d)) === ((x->a) & (x->b)) | ((x->c) & (x->d))
        """
        # if not value.is_true():
        for clause in self.cnf:
            for atom in clause:
                atom.saturate(value)
        """Atoms are shared between CNF and DNF"""

    def formula(self, formulatype: FormulaOutput = FormulaOutput.CNF) -> Union[
        Tuple[str, Typeset], Tuple[List[str], Typeset]]:
        """Generate the formula"""

        if formulatype == FormulaOutput.CNF:
            return LogicTuple.and_(
                [LogicTuple.or_([atom.formula() for atom in clause], brakets=True) for clause in self.cnf],
                brackets=False)

        if formulatype == FormulaOutput.ListCNF:
            return [Logic.or_([atom.string for atom in clause]) for clause in self.cnf], self.typeset

        if formulatype == FormulaOutput.DNF:
            return LogicTuple.or_(
                [LogicTuple.and_([atom.formula() for atom in clause], brackets=True) for clause in self.dnf],
                brakets=False)

    def __and__(self, other: Formula) -> Formula:
        """self & other
        Returns a new Specification with the conjunction with other"""
        new_ltl = deepcopy(self)
        new_ltl &= other
        return new_ltl

    def __or__(self, other: Formula) -> Formula:
        """self | other
        Returns a new Specification with the disjunction with other"""
        new_ltl = deepcopy(self)
        new_ltl |= other
        return new_ltl

    def __invert__(self) -> Formula:
        """Returns a new Specification with the negation of self"""

        new_ltl = deepcopy(self)

        """Negate all atoms"""
        for atom in new_ltl.atoms:
            atom.negate()

        """Swap CNF with DNF"""
        new_ltl.__cnf, new_ltl.__dnf = new_ltl.dnf, new_ltl.cnf

        return new_ltl

    def __rshift__(self, other: Union[Formula, Atom]) -> Formula:
        """>>
        Returns a new Specification that is the result of self -> other (implies)
        NOT self OR other"""
        from specification.atom import Atom
        if isinstance(other, Atom):
            other = Formula(other)

        if self.is_true():
            return other

        new_ltl = ~ self

        return new_ltl | other

    def __lshift__(self, other: Union[Formula, Atom]) -> Formula:
        """<<
        Returns a new Specification that is the result of other -> self (implies)
        NOT other OR self"""
        from specification.atom import Atom
        if isinstance(other, Atom):
            other = Formula(other)

        new_ltl = ~ other

        return new_ltl | self

    def __iand__(self, other: Union[Formula, Atom]) -> Formula:
        """self &= other
        Modifies self with the conjunction with other"""
        from specification.atom import Atom
        if isinstance(other, Atom):
            other = Formula(other)

        if other.is_false():
            new_atom = Atom("FALSE")
            self.__cnf: List[Set[Atom]] = [{new_atom}]
            self.__dnf: List[Set[Atom]] = [{new_atom}]
            return self

        if other.is_true():
            return self

        if other.is_true():
            self.__cnf = other.cnf
            self.__dnf = other.dnf
            return self

        if self.is_true():
            new_other = deepcopy(other)
            self.__cnf: List[Set[Atom]] = new_other.cnf
            self.__dnf: List[Set[Atom]] = new_other.dnf
            return self

        new_other = deepcopy(other)

        """Mutex Rules necessary for Satisfiability Check"""
        mutex_rules = Atom.extract_mutex_rules(self.typeset | other.typeset)

        """Cartesian product between the two dnf"""
        temp_dnf = []
        for a, b in itertools.product(self.dnf, new_other.dnf):

            new_set = a | b

            check_formula = LogicTuple.and_([f.formula() for f in new_set])

            """Adding Rules"""
            if mutex_rules is not None:
                check_formula = LogicTuple.and_([check_formula, mutex_rules.formula()])

            if Nuxmv.check_satisfiability(check_formula):
                temp_dnf.append(new_set)

        if len(temp_dnf) == 0:
            raise NotSatisfiableException(self, other, mutex_rules)
        else:
            self.__dnf = temp_dnf

        """Append to list if not already there"""
        for other_elem in new_other.cnf:
            if other_elem not in self.cnf:
                self.__cnf.append(other_elem)

        return self

    def __ior__(self, other: Union[Formula, Atom]) -> Formula:
        """self |= other
        Modifies self with the disjunction with other"""
        from specification.atom import Atom
        if isinstance(other, Atom):
            other = Formula(other)

        if self.is_true():
            return self

        if other.is_true():
            new_atom = Atom("TRUE")
            self.__cnf: List[Set[Atom]] = [{new_atom}]
            self.__dnf: List[Set[Atom]] = [{new_atom}]
            return self

        if other.is_false():
            return self

        new_other = deepcopy(other)

        """Cartesian product between the two cnf"""
        temp_cnf = []
        for a, b in itertools.product(self.cnf, new_other.cnf):

            new_set = a | b

            check_formula = LogicTuple.or_([f.formula() for f in new_set])
            if not Nuxmv.check_validity(check_formula):
                temp_cnf.append(new_set)
            else:
                pass

        if len(temp_cnf) == 0:
            """Result is TRUE"""
            new_atom = Atom("TRUE")
            self.__cnf: List[Set[Atom]] = [{new_atom}]
            self.__dnf: List[Set[Atom]] = [{new_atom}]
            return self
        else:
            self.__cnf = temp_cnf

        """Append to list if not already there"""
        for other_elem in new_other.dnf:
            if other_elem not in self.dnf:
                self.__dnf.append(other_elem)

        return self
