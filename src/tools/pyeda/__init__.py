from enum import Enum, auto
from typing import Dict

import pygraphviz as pgv
from pyeda.boolalg.expr import (
    IfThenElseOp,
    ImpliesOp,
    Literal,
    NaryOp,
    NotOp,
    One,
    Zero,
    expr,
)

from tools.logic import Logic


class Atom:
    pass


class Pyeda:
    class Output(Enum):
        SPOT_str = auto()
        PYEDA = auto()
        PYEDA_str = auto()

    def __init__(self, formula: str, atoms_dictionary: Dict[str, Atom]):

        formula = formula.replace("!", "~")
        print(expr(formula, simplify=True))
        print(expr(formula).to_nnf())
        self.__pyeda = expr(formula)
        self.__atoms_dictionary = atoms_dictionary
        self.__cnf = self.__pyeda.to_cnf()
        self.__dnf = self.__pyeda.to_dnf()

        self.to_spot()

    def represent(self, output: Output = Output.SPOT_str):
        if output == Pyeda.Output.SPOT_str:
            return self.__pyeda.to_str()
        elif output == Pyeda.Output.PYEDA:
            return self.__pyeda
        elif output == Pyeda.Output.PYEDA_str:
            return str(self.__pyeda)

    @property
    def atoms_dictionary(self):
        return self.__atoms_dictionary

    @property
    def dnf(self):
        return self.__dnf

    @property
    def cnf(self):
        return self.__cnf

    def to_spot(self):
        graph = pgv.AGraph(string=self.__pyeda.to_dot())
        labels = set()
        for n in graph.nodes():
            for label in n.attr["label"].split(","):
                if label != "":
                    labels.add(label)

        print(e for e in labels)

        operation_graph = dict()

        for (src, tgt) in graph.edges():
            if tgt in operation_graph.keys():
                operation_graph[tgt].add(src)
            else:
                operation_graph[tgt] = {src}

        print(operation_graph)

        spot_str = Pyeda.build_graph(operation_graph)
        print(spot_str)
        print("ok")

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
    def print_graph(operation_graph):
        for j, (key, values) in enumerate(operation_graph.items()):
            print(
                "\t" * j
                + f"{key.attr['label']} -> {[elem.attr['label'] for elem in values]}"
            )

    @staticmethod
    def build_graph(operation_graph, l=0) -> str:
        print(f"\nL={l}")
        print(Pyeda.print_graph(operation_graph))
        key = list(operation_graph.keys())[l]
        print(
            f"{key.attr['label']} -> {[elem.attr['label'] for elem in operation_graph[key]]}"
        )
        if Pyeda.are_all_atoms(operation_graph[key]):
            parent_index = Pyeda.get_parent_index(operation_graph, key)
            new_label = Pyeda.combine_atoms(
                atoms=operation_graph[key], operation=key.attr["label"]
            )
            key.attr["label"] = new_label
            key.attr["shape"] = "box"
            print("CIAO" + key.attr["label"])
            if parent_index is not None:
                del operation_graph[key]
                return Pyeda.build_graph(operation_graph, parent_index)
            else:
                return key.attr["label"]
        else:
            print("skip")
            return Pyeda.build_graph(operation_graph, l + 1)

    def to_spot_old(self, name="EXPR"):  # pragma: no cover
        """Convert to DOT language representation."""
        parts = ["graph", name, "{", "rankdir=BT;"]
        for ex in self.__pyeda.iter_dfs():
            exid = ex.node.id()
            if ex is Zero:
                parts += [f"n{exid} [label=0,shape=box];"]
            elif ex is One:
                parts += [f"n{exid} [label=1,shape=box];"]
            elif isinstance(ex, Literal):
                parts += [f'n{exid} [label="{ex}",shape=box];']
            else:
                parts += [f"n{exid} [label={ex.ASTOP},shape=circle];"]
        for ex in self.__pyeda.iter_dfs():
            exid = ex.node.id()
            if isinstance(ex, NotOp):
                parts += [f"n{ex.x.node.id()} -- n{exid};"]
            elif isinstance(ex, ImpliesOp):
                p, q = ex.xs
                parts += [f"n{p.node.id()} -- n{exid} [label=p];"]
                parts += [f"n{q.node.id()} -- n{exid} [label=q];"]
            elif isinstance(ex, IfThenElseOp):
                s, d1, d0 = ex.xs
                parts += [f"n{s.node.id()} -- n{exid} [label=s];"]
                parts += [f"n{d1.node.id()} -- n{exid} [label=d1];"]
                parts += [f"n{d0.node.id()} -- n{exid} [label=d0];"]
            elif isinstance(ex, NaryOp):
                for x in ex.xs:
                    parts += [f"n{x.node.id()} -- n{exid};"]
        parts.append("}")
        return " ".join(parts)
