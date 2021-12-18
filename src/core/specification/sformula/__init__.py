from __future__ import annotations

import hashlib
from copy import deepcopy
from enum import Enum, auto

import spot
from treelib import Tree

from core.patterns import Pattern
from core.specification import Specification
from core.typeset import Typeset
from tools.pyeda import Pyeda
from tools.spot import Spot


class Sformula(Specification):
    class Output(Enum):
        SPOT_str = auto()
        CNF_str = auto()
        DNF_str = auto()
        CNF_atoms = auto()
        DNF_atoms = auto()

    def __init__(
        self,
        formula: str | Pattern = None,
        boolean_formula: Pyeda = None,
        typeset: Typeset = None,
        kind: Specification.Kind = None,
        atom_hash: str = None,
    ):
        """We can build a Sformula from scratch (str, or Pattern) or from an
        existing Pyeda."""
        if (formula is None and boolean_formula is None) or (
            formula is not None and boolean_formula is not None
        ):
            raise AttributeError

        self.__spot_formula = None
        self.__kind = kind
        self.__ltl_tree = None
        self.__atoms_tree = None
        self.__atoms_dictionary = None
        self.__atom_hash = None
        self.__ltl_tree = None
        self.__boolean_formula = None
        self.__atoms_dictionary = None

        if kind is None:
            self.__kind = Specification.Kind.UNDEFINED

        if formula is not None:
            spot_formula = spot.formula(str(formula))
            spot_formula = spot.simplify(spot_formula)
            spot_formula = Spot.transform_tree(spot_formula)
            self.__spot_formula = spot_formula

            if typeset is None:
                self.__typeset = Typeset.generate_typeset(
                    Spot.extract_ap(self.__spot_formula)
                )
            else:
                s_typeset = Spot.extract_ap(formula)
                set_of_types = set(
                    filter((lambda x: x.name in s_typeset), typeset.values())
                )
                self.__typeset = Typeset(set_of_types)

            if atom_hash is not None:
                self.__atom_hash = atom_hash
            else:
                # Generate LTL Tree
                self.__ltl_tree = Tree()
                self.__gen_ltl_tree(tree=self.__ltl_tree)

                # Generate Atom Tree
                self.__atoms_dictionary = dict()
                self.__atoms_tree = Tree()
                self.__gen_atom_tree(tree=self.__atoms_tree)

                boolean_formula = deepcopy(self.__spot_formula.to_str())
                for key, value in self.__atoms_dictionary.items():
                    boolean_formula = boolean_formula.replace(
                        value["formula"].to_str(), key
                    )

                self.__boolean_formula = Pyeda(
                    boolean_formula, atoms_dictionary=self.__atoms_dictionary
                )

        elif boolean_formula is not None:
            self.__boolean_formula = boolean_formula
            self.__atoms_dictionary = boolean_formula.atoms_dictionary
            # TODO: we might want to change that to reflect the boolean formula structure

    def represent(self, output_type: Sformula.Output = Output.SPOT_str):
        if output_type == Sformula.Output.SPOT_str:
            return str(self.__spot_formula)

    @property
    def atom(self):
        return self.__atom_hash is not None

    @property
    def hash(self):
        if self.atom:
            return self.__atom_hash
        else:
            raise Exception("The formula is not an atom")

    @property
    def spot(self):
        return self.__spot_formula

    @property
    def boolean(self):
        return self.__boolean_formula

    @property
    def typeset(self):
        return self.__typeset

    @property
    def tree(self):
        if not self.atom:
            return self.__ltl_tree
        else:
            raise Exception("The formula an atom")

    @property
    def atoms(self):
        if not self.atom:
            return self.__atoms_tree
        else:
            raise Exception("The formula an atom")

    def __gen_ltl_tree(self, tree: Tree, formula=None, parent=None):
        if formula is None:
            formula = self.__spot_formula
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
                    self, formula=subformula, tree=tree, parent=node.identifier
                )

    def __gen_atom_tree(self, tree: Tree = None, formula=None, parent=None):
        if formula is None:
            formula = self.__spot_formula

        if (
            formula.kindstr() == "G"
            or formula.kindstr() == "F"
            or formula.kindstr() == "X"
            or formula.kindstr() == "U"
        ):
            s_typeset = Spot.extract_ap(formula)
            set_of_types = set(
                filter((lambda x: x.name in s_typeset), self.__typeset.values())
            )
            f_typeset = Typeset(set_of_types)
            f_string = formula.to_str()
            hash = f"a{hashlib.sha1(f_string.encode('utf-8')).hexdigest()}"[0:5]
            atom = Sformula(
                formula=formula, kind=self.__kind, typeset=f_typeset, atom_hash=hash
            )
            data = {"formula": formula, "operator": formula.kindstr(), "atom": atom}
            tree.create_node(
                tag=f"ATOM\t-->\t({formula}\t[{hash}])",
                parent=parent,
                data=data,
            )
            self.__atoms_dictionary[hash] = data
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
                        self,
                        formula=subformula,
                        tree=tree,
                        parent=node.identifier,
                    )

    def __and__(self: Sformula, other: Sformula) -> Sformula:
        """self & other Returns a new Sformula with the conjunction with
        other."""
        new_formula = deepcopy(self)
        new_formula &= other
        return new_formula

    def __or__(self: Sformula, other: Sformula) -> Sformula:
        """self | other Returns a new Sformula with the disjunction with
        other."""
        new_formula = deepcopy(self)
        new_formula |= other
        return new_formula

    def __invert__(self: Sformula) -> Sformula:
        """Returns a new Sformula with the negation of self."""
        new_formula = deepcopy(self)
        new_formula &= other
        return new_formula

    def __rshift__(self: Sformula, other: Sformula) -> Sformula:
        """>> Returns a new Sformula that is the result of self -> other
        (implies)"""

    def __lshift__(self: Sformula, other: Sformula) -> Sformula:
        """<< Returns a new Sformula that is the result of other -> self
        (implies)"""

    def __iand__(self: Sformula, other: Sformula) -> Sformula:
        """self &= other Modifies self with the conjunction with other."""

    def __ior__(self: Sformula, other: Sformula) -> Sformula:
        """self |= other Modifies self with the disjunction with other."""


if __name__ == "__main__":
    phi = "! z & G(a & b | G(k & l)) & F(c | !d) & (X(e & f) | !X(g | h)) & (l U p)"
    sformula = Sformula(phi)
    print(sformula.tree)
    print(sformula.atoms)
    print(sformula.boolean.represent(Pyeda.Output.PYEDA.to_cnf()))

    # aps = Sformula.extract_ap(sformula.spot)
    # print(aps)
