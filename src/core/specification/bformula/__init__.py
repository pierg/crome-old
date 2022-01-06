from __future__ import annotations

from copy import deepcopy
from enum import Enum, auto
from typing import List

import pygraphviz as pgv
from pyeda.boolalg.expr import AndOp, Expression, OrOp, expr
from pyeda.boolalg.minimization import espresso_exprs

from tools.logic import Logic


class BooleansNotSATException(Exception):
    def __init__(self, formula: str):
        self.formula = formula
        print(f"{formula}\nNOT SAT")


class Bool:
    class Output(Enum):
        SPOT_str = auto()
        PYEDA = auto()
        PYEDA_str = auto()

    def __init__(self, formula: str | Expression):

        if isinstance(formula, str):
            formula = formula.replace("!", "~")
            expression = expr(formula)
        elif isinstance(formula, Expression):
            expression = formula
        else:
            raise AttributeError

        if expression.satisfy_one() is None:
            raise BooleansNotSATException(str(expression))

        """Espresso Minimization
        Notice that the espresso_exprs function returns a tuple.
        The reason is that this function can minimize multiple input functions simultaneously."""
        if expression.is_one():
            self.__expression = expression
        else:
            self.__expression = espresso_exprs(expression.to_dnf())[0]

    def __deepcopy__(self: Bool, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        try:
            for k, v in self.__dict__.items():
                if "_Bool__expression" in k:
                    setattr(result, k, expr(self.expression))
                else:
                    setattr(result, k, deepcopy(v, memo))
        except Exception:
            print(k)
        return result

    @property
    def expression(self):
        return self.__expression

    def represent(self, output: Output = Output.SPOT_str):
        if output == Bool.Output.SPOT_str:
            return self.to_spot()
        elif output == Bool.Output.PYEDA:
            return self.__expression
        elif output == Bool.Output.PYEDA_str:
            return str(self.__expression)

    def __str__(self):
        return self.represent(Bool.Output.PYEDA_str)

    @property
    def dnf(self) -> List[set[str]]:

        dnf_list = []
        dnf = expr(self.__expression.to_dnf())
        if isinstance(dnf, OrOp):
            for clause in dnf.xs:
                atoms = set()
                if isinstance(clause, AndOp):
                    for atom in clause.xs:
                        atoms.add(str(atom))
                else:
                    atoms.add(str(clause))
                dnf_list.append(atoms)
        elif isinstance(dnf, AndOp):
            atoms = set()
            for atom in dnf.xs:
                atoms.add(str(atom))
            dnf_list.append(atoms)
        else:
            dnf_list.append({str(dnf)})
        return dnf_list

    @property
    def cnf(self) -> List[set[str]]:

        cnf_list = []
        cnf = expr(self.__expression.to_cnf())
        if isinstance(cnf, AndOp):
            for clause in cnf.xs:
                atoms = set()
                if isinstance(clause, OrOp):
                    for atom in clause.xs:
                        atoms.add(str(atom))
                else:
                    atoms.add(str(clause))
                cnf_list.append(atoms)
        elif isinstance(cnf, OrOp):
            atoms = set()
            for atom in cnf.xs:
                atoms.add(str(atom))
            cnf_list.append(atoms)
        else:
            cnf_list.append({str(cnf)})
        return cnf_list

    def to_spot(self) -> str:
        graph = pgv.AGraph(string=self.__expression.to_dot())
        labels = set()
        for n in graph.nodes():
            for label in n.attr["label"].split(","):
                if label != "":
                    labels.add(label)

        if len(labels) == 1:
            return list(labels)[0]

        operation_graph = dict()

        for (src, tgt) in graph.edges():
            if tgt in operation_graph.keys():
                operation_graph[tgt].add(src)
            else:
                operation_graph[tgt] = {src}

        # print(operation_graph)

        spot_str = Bool.build_graph(operation_graph)
        spot_str = spot_str.replace("~", "!")
        return spot_str

    @staticmethod
    def are_all_atoms(elems) -> bool:
        for e in elems:
            if e.attr["shape"] == "circle":
                return False
        return True

    @staticmethod
    def combine_atoms(atoms, operation) -> str:
        if operation == "and":
            return Logic.and_([a.attr["label"] for a in atoms], brackets=True)
        elif operation == "or":
            return Logic.or_([a.attr["label"] for a in atoms])

    @staticmethod
    def get_parent_index(operation_graph, key):
        for j, (k, values) in enumerate(operation_graph.items()):
            if key in values:
                return j

    @staticmethod
    def operation_graph_to_str(operation_graph) -> str:
        ret = ""
        for j, (key, values) in enumerate(operation_graph.items()):
            ret += (
                "\t" * j
                + f"{key.attr['label']} -> {[elem.attr['label'] for elem in values]}\n"
            )
        return ret

    @staticmethod
    def build_graph(operation_graph) -> str:
        # print(Pyeda.operation_graph_to_str(operation_graph))
        key = None
        for k in operation_graph.keys():
            if Bool.are_all_atoms(operation_graph[k]):
                key = k

        if len(operation_graph.keys()) == 1:
            return Bool.combine_atoms(
                atoms=operation_graph[key], operation=key.attr["label"]
            )

        if key is not None:
            # print(
            #     f"SELECTED\n{key.attr['label']} -> {[elem.attr['label'] for elem in operation_graph[key]]}"
            # )
            new_label = Bool.combine_atoms(
                atoms=operation_graph[key], operation=key.attr["label"]
            )
            key.attr["label"] = new_label
            key.attr["shape"] = "box"

            del operation_graph[key]

        return Bool.build_graph(operation_graph)

    def __and__(self: Bool, other: Bool) -> Bool:
        """self & other Returns a new Pyeda with the conjunction with other."""
        return Bool(self.expression & other.expression)

    def __or__(self: Bool, other: Bool) -> Bool:
        """self | other Returns a new Pyeda with the disjunction with other."""
        return Bool(self.expression | other.expression)

    def __invert__(self: Bool) -> Bool:
        """Returns a new Pyeda with the negation of self."""
        return Bool(~self.__expression)

    def __rshift__(self: Bool, other: Bool) -> Bool:
        """>> Returns a new Pyeda that is the result of self -> other
        (implies)"""
        return Bool(self.expression >> other.expression)

    def __lshift__(self: Bool, other: Bool) -> Bool:
        """<< Returns a new Pyeda that is the result of other -> self
        (implies)"""
        return Bool(other.expression >> self.expression)

    def __iand__(self: Bool, other: Bool) -> Bool:
        """self &= other Modifies self with the conjunction with other."""
        self.__expression = self.__expression & other.expression
        return self

    def __ior__(self: Bool, other: Bool) -> Bool:
        """self |= other Modifies self with the disjunction with other."""
        self.__expression = expr(self.__expression | other.expression)
        return self


if __name__ == "__main__":
    # f = Pyeda("((f | b) & s | g) & ((f | b) & s | g)")
    # print(f)
    # print(f.to_spot())
    #
    # g1 = Pyeda("((f | b) & s | g)")
    # g2 = Pyeda("((f | b) & s | g)")
    # g = g1 & g2
    # print(g)
    # print(g.to_spot())

    # f = Pyeda("(!f | !b) & !(s | g)")
    # cnf = f.cnf
    # print(cnf)

    f = Bool("c")
    b = Bool("b")
    c = b | ~f
