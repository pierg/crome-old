import itertools
from typing import List, Tuple

from tools.logic import Logic


class SynthesisInfo:

    def __init__(self,
                 assumptions: List[str] = None,
                 a_liveness: List[str] = None,
                 a_mutex: List[str] = None,
                 guarantees: List[str] = None,
                 g_mutex: List[str] = None,
                 g_adjacency: List[str] = None,
                 inputs: List[str] = None,
                 outputs: List[str] = None):
        self.__assumptions = assumptions
        self.__a_liveness = a_liveness
        self.__a_mutex = a_mutex
        self.__guarantees = guarantees
        self.__g_mutex = g_mutex
        self.__g_adjacency = g_adjacency
        self.__inputs = inputs
        self.__outputs = outputs

    @property
    def assumptions(self):
        return self.__assumptions

    @property
    def a_liveness(self):
        return self.__a_liveness

    @property
    def a_mutex(self):
        return self.__a_mutex

    @property
    def guarantees(self):
        return self.__guarantees

    @property
    def g_mutex(self):
        return self.__g_mutex

    @property
    def g_adjacency(self):
        return self.__g_adjacency

    @property
    def inputs(self):
        return self.__inputs

    @property
    def outputs(self):
        return self.__outputs

    def get_strix_inputs(self) -> Tuple[str, str, str, str]:

        a = Logic.and_(list(itertools.chain(
            self.__assumptions,
            self.__a_mutex,
            self.__a_liveness
        )))
        from tools.strings import StringMng
        a = StringMng.strix_syntax_fix(a)

        g = Logic.and_(list(itertools.chain(
            self.__guarantees,
            self.__g_mutex,
            self.__g_adjacency
        )))
        g = StringMng.strix_syntax_fix(g)

        i = " ,".join(self.__inputs)
        o = " ,".join(self.__outputs)

        return a, g, i, o

    def save_to_file(path: str):
        pass
