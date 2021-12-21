from __future__ import annotations

from enum import Enum, auto
from typing import List

import pygraphviz as pgv
from pyeda.boolalg.expr import AndOp, Expression, OrOp, expr
from pyeda.boolalg.minimization import espresso_exprs

from tools.logic import Logic


class Atom:
    pass


class Pyeda:
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

        """Espresso Minimization
        Notice that the espresso_exprs function returns a tuple.
        The reason is that this function can minimize multiple input functions simultaneously."""
        self.__expression = espresso_exprs(expression.to_dnf())[0]

    @property
    def expression(self):
        return self.__expression

    def represent(self, output: Output = Output.SPOT_str):
        if output == Pyeda.Output.SPOT_str:
            return self.to_spot()
        elif output == Pyeda.Output.PYEDA:
            return self.__expression
        elif output == Pyeda.Output.PYEDA_str:
            return str(self.__expression)

    def __str__(self):
        return self.represent(Pyeda.Output.PYEDA_str)

    @property
    def dnf(self) -> List[set[str]]:

        dnf_list = []
        for clause in expr(self.__expression.to_dnf()).xs:
            if isinstance(clause, AndOp):
                atoms = set()
                for atom in clause.xs:
                    atoms.add(str(atom))
                dnf_list.append(atoms)
            else:
                dnf_list.append(str(clause))

        return dnf_list

    @property
    def cnf(self) -> List[set[str]]:

        cnf_list = []
        print(self.__expression.to_cnf())
        for clause in expr(self.__expression.to_cnf()).xs:
            atoms = set()
            if isinstance(clause, OrOp):
                for atom in clause.xs:
                    atoms.add(str(atom))
            else:
                atoms.add(str(clause))
            cnf_list.append(atoms)
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

        spot_str = Pyeda.build_graph(operation_graph)
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
            if Pyeda.are_all_atoms(operation_graph[k]):
                key = k

        if len(operation_graph.keys()) == 1:
            return Pyeda.combine_atoms(
                atoms=operation_graph[key], operation=key.attr["label"]
            )

        if key is not None:
            # print(
            #     f"SELECTED\n{key.attr['label']} -> {[elem.attr['label'] for elem in operation_graph[key]]}"
            # )
            new_label = Pyeda.combine_atoms(
                atoms=operation_graph[key], operation=key.attr["label"]
            )
            key.attr["label"] = new_label
            key.attr["shape"] = "box"

            del operation_graph[key]

        return Pyeda.build_graph(operation_graph)

    def __and__(self: Pyeda, other: Pyeda) -> Pyeda:
        """self & other Returns a new Pyeda with the conjunction with other."""
        return Pyeda(self.expression & other.expression)

    def __or__(self: Pyeda, other: Pyeda) -> Pyeda:
        """self | other Returns a new Pyeda with the disjunction with other."""
        return Pyeda(self.expression | other.expression)

    def __invert__(self: Pyeda) -> Pyeda:
        """Returns a new Pyeda with the negation of self."""
        return Pyeda(~self.__expression)

    def __rshift__(self: Pyeda, other: Pyeda) -> Pyeda:
        """>> Returns a new Pyeda that is the result of self -> other
        (implies)"""
        return Pyeda(self.expression >> other.expression)

    def __lshift__(self: Pyeda, other: Pyeda) -> Pyeda:
        """<< Returns a new Pyeda that is the result of other -> self
        (implies)"""
        return Pyeda(other.expression >> self.expression)

    def __iand__(self: Pyeda, other: Pyeda) -> Pyeda:
        """self &= other Modifies self with the conjunction with other."""
        self.__expression = self.__expression & other.expression
        return self

    def __ior__(self: Pyeda, other: Pyeda) -> Pyeda:
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

    f = Pyeda("(!f | !b) & !(s | g)")
    cnf = f.cnf
    print(cnf)
