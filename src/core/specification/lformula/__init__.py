from __future__ import annotations

import hashlib
from copy import deepcopy
from enum import Enum, auto
from typing import List, Set

import spot
from treelib import Tree

from core.patterns import Pattern
from core.specification import Specification, SpecNotSATException
from core.specification.bformula import Bool
from core.typeset import Typeset
from tools.logic import Logic
from tools.spot import Spot


class LTLNotSATException(SpecNotSATException):
    def __init__(self, formula: LTL):
        self.formula = formula
        super().__init__(formula)


class LTL(Specification):
    class Output(Enum):
        SPOT_str = auto()
        CNF_str = auto()
        DNF_str = auto()
        SUMMARY = auto()

    class TreeType(Enum):
        LTL = auto()
        BOOLEAN = auto()

    def __init__(
        self,
        formula: str | Pattern = None,
        boolean_formula: Bool = None,
        atoms_dictionary: dict[str, LTL] = None,
        typeset: Typeset = None,
        kind: Specification.Kind = None,
        atom_hash: str = None,
    ):
        """We can build a Sformula from scratch (str, or Pattern) or from an
        existing Pyeda."""

        self.__spot_formula = None
        self.__kind = kind
        self.__ltl_tree = None
        self.__atoms_tree = None
        self.__atoms_dictionary = None
        self.__atom_hash = atom_hash
        self.__ltl_tree = None
        self.__boolean_formula = None

        if kind is None:
            self.__kind = Specification.Kind.UNDEFINED

        self.__init__ltl_formula(formula, typeset)
        self.__init__atoms_formula(boolean_formula, atoms_dictionary)

    def __init__ltl_formula(self, formula, typeset):
        """Building the LTL formula and tree."""
        self.__original_formula = str(formula)
        spot_formula = spot.formula(self.__original_formula)
        spot_formula = spot.simplify(spot_formula)
        spot_formula = Spot.transform_tree(spot_formula)

        """Check if satisfiable"""
        if str(spot_formula) == "0":
            raise LTLNotSATException(self)

        self.__spot_formula = spot_formula

        if typeset is None:
            self.__typeset = Typeset.generate_typeset(
                Spot.extract_ap(self.__spot_formula)
            )
        else:
            s_typeset = Spot.extract_ap(self.__spot_formula)
            set_of_types = set(
                filter((lambda x: x.name in s_typeset), typeset.values())
            )
            self.__typeset = Typeset(set_of_types)

        # Generate LTL Tree
        self.__ltl_tree = Tree()
        self.__gen_ltl_tree(tree=self.__ltl_tree)

    def __init__atoms_formula(self, boolean_formula, atoms_dictionary):
        """Building the ATOMS formula and tree."""
        if boolean_formula is None and atoms_dictionary is None:
            # Generate Atom Tree
            self.__atoms_dictionary = dict()
            self.__atoms_tree = Tree()
            self.__gen_atom_tree(tree=self.__atoms_tree)
            self.__boolean_formula = Bool(self.__translate_ltl_to_bool())

        else:
            """Create a 'boolean' spot formula."""
            self.__boolean_formula = boolean_formula
            self.__atoms_dictionary = atoms_dictionary

            """Trick to generate atoms tree"""
            bool_spot = spot.formula(boolean_formula.to_spot())
            self.__atoms_dictionary = dict()
            self.__atoms_tree = Tree()
            self.__gen_atom_tree(tree=self.__atoms_tree, spot_f=bool_spot)

    def represent(self, output_type: LTL.Output = Output.SUMMARY) -> str:
        if output_type == LTL.Output.SPOT_str:
            return str(self.__spot_formula)
        elif output_type == LTL.Output.SUMMARY:
            cnf = "\n".join([Logic.or_([e.string for e in elem]) for elem in self.cnf])
            dnf = "\n".join([Logic.and_([e.string for e in elem]) for elem in self.dnf])
            ret = (
                f"\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
                f"LTL SIMPLIFIED\n"
                f"{self.to_ltl}\n\n"
                f"BOOLEAN REPRESENTATION\n"
                f"{self.to_bool}\n\n"
                f"LTL EXTENDED (from booleans)\n"
                f"{self.__translate_bool_to_ltl()}\n\n"
                # f"LTL CNF (from booleans)\n"
                # f"{self.__normal_form_to_str(Sformula.Output.CNF_str)}\n\n"
                # f"LTL DNF (from booleans)\n"
                # f"{self.__normal_form_to_str(Sformula.Output.DNF_str)}\n"
                f"LTL CNF (from booleans)\n"
                f"{cnf}\n\n"
                f"LTL DNF (from booleans)\n"
                f"{dnf}\n"
                f"+++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n"
            )
            return ret

    @property
    def is_atom(self) -> bool:
        return self.__atom_hash is not None

    @property
    def to_ltl(self) -> str:
        if self.__spot_formula.kindstr() == "U":
            return f"({str(self.__spot_formula)})"
        return str(self.__spot_formula)

    @property
    def to_bool(self) -> str:
        return str(self.__boolean_formula.to_spot())

    @property
    def original_formula(self) -> str:
        return self.__original_formula

    @property
    def hash(self):
        if self.is_atom:
            return self.__atom_hash
        else:
            raise Exception("The formula is not an atom")

    @property
    def typeset(self):
        return self.__typeset

    @property
    def atoms_dictionary(self) -> dict:
        return self.__atoms_dictionary

    @property
    def cnf(self) -> List[Set[LTL]]:
        ret = []
        for clause in self.__boolean_formula.cnf:
            clause_set = set()
            for atom in clause:
                if atom.startswith("~"):
                    clause_set.add(~self.__atoms_dictionary[atom[1:]])
                else:
                    clause_set.add(self.__atoms_dictionary[atom])
            ret.append(clause_set)
        return ret

    @property
    def dnf(self) -> List[Set[LTL]]:
        ret = []
        for clause in self.__boolean_formula.dnf:
            clause_set = set()
            for atom in clause:
                if atom.startswith("~"):
                    clause_set.add(~self.__atoms_dictionary[atom[1:]])
                else:
                    clause_set.add(self.__atoms_dictionary[atom])
            ret.append(clause_set)
        return ret

    @property
    def string(self: LTL) -> str:
        return self.to_ltl

    def __normal_form_to_str(self, kind: Output = Output.CNF_str):
        if kind == LTL.Output.CNF_str:
            return Logic.and_(
                [
                    Logic.or_([atom.to_ltl for atom in clause], brackets=True)
                    for clause in self.cnf
                ],
                brackets=False,
            )
        elif kind == LTL.Output.DNF_str:
            return Logic.or_(
                [
                    Logic.and_([atom.to_ltl for atom in clause], brackets=True)
                    for clause in self.dnf
                ],
                brackets=False,
            )
        else:
            raise AttributeError

    def __translate_ltl_to_bool(self, formula: str = None) -> str:
        if isinstance(formula, str):
            boolean_formula_str = formula
        else:
            boolean_formula_str = deepcopy(self.__spot_formula.to_str())
        for key, value in self.__atoms_dictionary.items():
            boolean_formula_str = boolean_formula_str.replace(
                value.represent(LTL.Output.SPOT_str), key
            )
        return boolean_formula_str

    def __translate_bool_to_ltl(self, formula: str = None) -> str:
        if isinstance(formula, str):
            ltl_formula_str = formula
        else:
            ltl_formula_str = deepcopy(self.__boolean_formula.to_spot())
        for key, value in self.__atoms_dictionary.items():
            ltl_formula_str = ltl_formula_str.replace(
                key, value.represent(LTL.Output.SPOT_str)
            )
        return ltl_formula_str

    def tree(self, tree_type: TreeType = TreeType.LTL) -> Tree:
        if tree_type == LTL.TreeType.LTL:
            return self.__ltl_tree
        elif tree_type == LTL.TreeType.BOOLEAN:
            return self.__atoms_tree
        else:
            raise AttributeError

    def __gen_ltl_tree(self, tree: Tree, spot_f=None, parent=None):
        if spot_f is None:
            spot_f = self.__spot_formula
        node = tree.create_node(
            tag=f"{spot_f.kindstr()}\t--\t({spot_f})",
            parent=parent,
            data={
                "formula": spot_f,
                "operator": spot_f.kindstr(),
                "n_children": spot_f.size(),
            },
        )

        if spot_f.size() > 0:
            for subformula in spot_f:
                LTL.__gen_ltl_tree(
                    self, spot_f=subformula, tree=tree, parent=node.identifier
                )

    def __create_atom_tree_node(self, tree, parent, spot_f, sformula, tag, hash):
        data = {
            "formula": str(spot_f),
            "operator": spot_f.kindstr(),
            "n_children": spot_f.size(),
            "lformula": sformula,
        }
        node = tree.create_node(
            tag=tag,
            parent=parent,
            data=data,
        )
        if hash is not None:
            self.__atoms_dictionary[hash] = sformula

        return node

    def __gen_atom_tree(
        self, tree: Tree = None, spot_f: spot.formula = None, parent=None
    ):
        if spot_f is None:
            spot_f = self.__spot_formula

        if self.is_atom:
            self.__create_atom_tree_node(
                tree=tree,
                spot_f=spot_f,
                parent=parent,
                sformula=self,
                tag=self.hash,
                hash=self.hash,
            )
            return

        s_typeset = Spot.extract_ap(spot_f)
        set_of_types = set(
            filter((lambda x: x.name in s_typeset), self.__typeset.values())
        )
        f_typeset = Typeset(set_of_types)
        f_string = spot_f.to_str()

        if (
            spot_f.kindstr() == "G"
            or spot_f.kindstr() == "F"
            or spot_f.kindstr() == "X"
            or spot_f.kindstr() == "U"
            or spot_f.kindstr() == "ap"
            or spot_f.kindstr() == "tt"
        ):
            if spot_f.kindstr() == "ap" or spot_f.kindstr() == "tt":
                hash_ = f_string
            else:
                hash_ = f"a{hashlib.sha1(f_string.encode('utf-8')).hexdigest()}"[0:5]

            if self.__spot_formula == spot_f:
                self.__atom_hash = hash_
                sformula = self
            else:
                sformula = LTL(
                    formula=spot_f, kind=self.__kind, typeset=f_typeset, atom_hash=hash_
                )

            self.__create_atom_tree_node(
                tree=tree,
                spot_f=spot_f,
                parent=parent,
                sformula=sformula,
                tag=hash_,
                hash=hash_,
            )

            return

        node = self.__create_atom_tree_node(
            tree=tree,
            spot_f=spot_f,
            parent=parent,
            sformula=self,
            tag=str(spot_f.kindstr()),
            hash=None,
        )

        if spot_f.size() > 0:
            for subformula in spot_f:
                LTL.__gen_atom_tree(
                    self,
                    spot_f=subformula,
                    tree=tree,
                    parent=node.identifier,
                )

    def __and__(self: LTL, other: LTL) -> LTL:
        """self & other Returns a new Sformula with the conjunction with
        other."""
        return LTL(
            formula=f"({self.to_ltl}) & ({other.to_ltl})",
            boolean_formula=self.__boolean_formula & other.__boolean_formula,
        )

    def __or__(self: LTL, other: LTL) -> LTL:
        """self | other Returns a new Sformula with the disjunction with
        other."""
        return LTL(
            formula=f"({self.to_ltl}) | ({other.to_ltl})",
            boolean_formula=self.__boolean_formula | other.__boolean_formula,
        )

    def __invert__(self: LTL) -> LTL:
        """Returns a new Sformula with the negation of self."""
        return LTL(formula=f"!({self.to_ltl})", boolean_formula=~self.__boolean_formula)

    def __rshift__(self: LTL, other: LTL) -> LTL:
        """>> Returns a new Sformula that is the result of self -> other
        (implies)"""
        return LTL(
            formula=f"({self.to_ltl}) -> ({other.to_ltl})",
            boolean_formula=self.__boolean_formula >> other.__boolean_formula,
        )

    def __lshift__(self: LTL, other: LTL) -> LTL:
        """<< Returns a new Sformula that is the result of other -> self
        (implies)"""
        return LTL(
            formula=f"({other.to_ltl}) -> ({self.to_ltl})",
            boolean_formula=other.__boolean_formula >> self.__boolean_formula,
        )

    def __iand__(self: LTL, other: LTL) -> LTL:
        """self &= other Modifies self with the conjunction with other."""
        self.__init__ltl_formula(
            formula=f"({self.to_ltl}) & ({other.to_ltl})",
            typeset=self.typeset | other.typeset,
        )
        self.__init__atoms_formula(
            boolean_formula=self.__boolean_formula & other.__boolean_formula,
            atoms_dictionary={**self.__atoms_dictionary, **other.__atoms_dictionary},
        )
        return self

    def __ior__(self: LTL, other: LTL) -> LTL:
        """self |= other Modifies self with the disjunction with other."""
        self.__init__ltl_formula(
            formula=f"({self.to_ltl}) | ({other.to_ltl})",
            typeset=self.typeset | other.typeset,
        )
        self.__init__atoms_formula(
            boolean_formula=self.__boolean_formula | other.__boolean_formula,
            atoms_dictionary={**self.__atoms_dictionary, **other.__atoms_dictionary},
        )
        return self


if __name__ == "__main__":
    phi = "! z & G(a & b | G(k & l)) & F(c | !d) & (X(e & f) | !X(g | h)) & (l U p)"
    sformula = LTL(phi)
    print(sformula.tree(LTL.TreeType.LTL))
    print(sformula.tree(LTL.TreeType.BOOLEAN))

    # print(lformula.tree)
    # print(lformula.atoms)
    # print(lformula.boolean.represent(Pyeda.Output.PYEDA.to_cnf()))

    # aps = Sformula.extract_ap(lformula.spot)
    # print(aps)
