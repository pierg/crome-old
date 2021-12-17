from __future__ import annotations

import hashlib
from copy import deepcopy
from typing import Set

import spot
from treelib import Tree

from core.specification import Specification
from core.specification.atom import Atom, AtomKind
from core.specification.enums import SpecKind
from core.typeset import Typeset
from tools.pyeda import Pyeda


class Sformula(Specification):
    def __init__(self, formula: str, typeset: Typeset = None):

        spot_formula = spot.formula(formula)
        spot_formula = spot.simplify(spot_formula)
        spot_formula = Sformula.apply_equalities(spot_formula)
        self.__spot_formula = spot_formula
        if typeset is None:
            self.__typeset = Typeset.generate_typeset(
                Sformula.extract_ap(self.__spot_formula)
            )

        (
            self.__ltl_tree,
            self.__atoms_tree,
            self.__atoms_dictionary,
        ) = self.__create_trees()
        print(self.__atoms_dictionary)
        self.__boolean_formula = self.__gen_boolean_formula()
        print(self.__boolean_formula.cnf)
        print(self.__boolean_formula.dnf)
        print("ciao")

    @property
    def formula(self):
        pass

    @property
    def spot(self):
        return self.__spot_formula

    @property
    def typeset(self):
        return self.__typeset

    @property
    def tree(self):
        return self.__ltl_tree

    @property
    def atoms(self):
        return self.__atoms_tree

    def __create_trees(self):
        tree = Tree()
        atoms_tree = Tree()
        atom_dictionary = dict()
        self.__gen_ltl_tree(self.__spot_formula, tree=tree)
        self.__gen_atom_tree(
            self.__spot_formula,
            typeset=self.__typeset,
            tree=atoms_tree,
            atom_dictionary=atom_dictionary,
        )
        return tree, atoms_tree, atom_dictionary

    def __gen_boolean_formula(self) -> Pyeda:
        boolean_formula = deepcopy(self.__spot_formula.to_str())
        for key, value in self.__atoms_dictionary.items():
            boolean_formula = boolean_formula.replace(value["formula"].to_str(), key)

        return Pyeda(boolean_formula)

    def swap_equalities(self):
        new_formula = self.apply_equalities(self.__spot_formula)
        self.__spot_formula = new_formula

    @staticmethod
    def apply_equalities(spot_formula):

        if spot_formula._is(spot.op_F):
            if spot_formula[0]._is(spot.op_Or):
                new_f = spot.formula.Or([spot.formula.F(sf) for sf in spot_formula[0]])
                return Sformula.apply_equalities(new_f)

        if spot_formula._is(spot.op_G):
            if spot_formula[0]._is(spot.op_And):
                new_f = spot.formula.And([spot.formula.G(sf) for sf in spot_formula[0]])
                return Sformula.apply_equalities(new_f)

        if spot_formula._is(spot.op_X):
            if spot_formula[0]._is(spot.op_And):
                new_f = spot.formula.And([spot.formula.X(sf) for sf in spot_formula[0]])
                return Sformula.apply_equalities(new_f)

            if spot_formula[0]._is(spot.op_Or):
                new_f = spot.formula.Or([spot.formula.X(sf) for sf in spot_formula[0]])
                return Sformula.apply_equalities(new_f)

        if Sformula.count_sugar(spot_formula) == 0:
            return spot_formula

        # Apply it recursively on any other operator's children
        return spot_formula.map(Sformula.apply_equalities)

    @staticmethod
    def __gen_ltl_tree(formula, tree: Tree, parent=None):
        node = tree.create_node(
            tag=f"{formula.kindstr()}\t--\t({formula})",
            parent=parent,
            data={
                "formula": formula,
                "operator": formula.kindstr(),
                "n_children": formula.size(),
            },
        )

        if formula.size() > 0:
            for subformula in formula:
                Sformula.__gen_ltl_tree(
                    formula=subformula, tree=tree, parent=node.identifier
                )

    @staticmethod
    def __gen_atom_tree(
        formula, tree: Tree, typeset: Typeset, atom_dictionary, parent=None
    ):
        if (
            formula.kindstr() == "G"
            or formula.kindstr() == "F"
            or formula.kindstr() == "X"
            or formula.kindstr() == "U"
        ):
            s_typeset = Sformula.extract_ap(formula)
            set_of_types = set(
                filter((lambda x: x.name in s_typeset), typeset.values())
            )
            f_typeset = Typeset(set_of_types)
            atom = Atom(formula=(str(formula), f_typeset), check=False)
            f_string = formula.to_str()
            hash = f"a{hashlib.sha1(f_string.encode('utf-8')).hexdigest()}"[0:5]
            data = {"formula": formula, "operator": formula.kindstr(), "atom": atom}
            tree.create_node(
                tag=f"ATOM\t-->\t({formula}\t[{hash}])",
                parent=parent,
                data=data,
            )
            atom_dictionary[hash] = data
        else:
            node = tree.create_node(
                tag=f"{formula.kindstr()}\t--\t({formula})",
                parent=parent,
                data={
                    "formula": formula,
                    "operator": formula.kindstr(),
                    "n_children": formula.size(),
                },
            )
            if formula.size() > 0:
                for subformula in formula:
                    Sformula.__gen_atom_tree(
                        formula=subformula,
                        tree=tree,
                        typeset=typeset,
                        atom_dictionary=atom_dictionary,
                        parent=node.identifier,
                    )

    @staticmethod
    def count_sugar(formula, n_sugar=0) -> int:
        if formula._is(spot.op_G) or formula._is(spot.op_F) or formula._is(spot.op_X):
            for subformula in formula:
                return Sformula.count_sugar(formula=subformula, n_sugar=n_sugar + 1)

        if formula.size() > 0:
            for subformula in formula:
                return Sformula.count_sugar(formula=subformula, n_sugar=n_sugar + 1)
        else:
            return n_sugar

    @staticmethod
    def extract_ap(formula, ap=None) -> Set[str]:
        if ap is None:
            ap = set()
        if formula._is(spot.op_ap):
            ap.add(str(formula))
        else:
            for subformula in formula:
                ap | Sformula.extract_ap(formula=subformula, ap=ap)
        return ap

    @property
    def spec_kind(self: Specification) -> SpecKind:
        pass

    def __and__(self: Specification, other: Specification) -> Specification:
        """self & other Returns a new Specification with the conjunction with
        other."""

    def __or__(self: Specification, other: Specification) -> Specification:
        """self | other Returns a new Specification with the disjunction with
        other."""

    def __invert__(self: Specification) -> Specification:
        """Returns a new Specification with the negation of self."""

    def __rshift__(self: Specification, other: Specification) -> Specification:
        """>> Returns a new Specification that is the result of self -> other
        (implies)"""

    def __lshift__(self: Specification, other: Specification) -> Specification:
        """<< Returns a new Specification that is the result of other -> self
        (implies)"""

    def __iand__(self: Specification, other: Specification) -> Specification:
        """self &= other Modifies self with the conjunction with other."""

    def __ior__(self: Specification, other: Specification) -> Specification:
        """self |= other Modifies self with the disjunction with other."""

    def contains_rule(self: Specification, other: AtomKind = None) -> bool:
        pass


if __name__ == "__main__":
    phi = "! z & G(a & b | G(k & l)) & F(c | !d) & (X(e & f) | !X(g | h)) & (l U p)"
    sformula = Sformula(phi)
    print(sformula.tree)
    print(sformula.atoms)

    # aps = Sformula.extract_ap(sformula.spot)
    # print(aps)
