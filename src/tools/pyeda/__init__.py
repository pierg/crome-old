from pyeda.boolalg.expr import expr


class Pyeda:
    def __init__(self, formula):

        print(expr(formula, simplify=False))
        print(expr(formula).to_nnf())
        self.__formula = expr(formula)
        self.__cnf = self.__formula.to_cnf()
        self.__dnf = self.__formula.to_dnf()

    @property
    def formula(self):
        return self.__formula

    @property
    def dnf(self):
        return self.__dnf

    @property
    def cnf(self):
        return self.__cnf


if __name__ == "__main__":

    eda_formula = Pyeda("( ~(a1 & a2) | (a3 & ~a4) | (a3 & ~a4) | (a3 & ~a4))")
    print(eda_formula.formula)
    print(eda_formula.dnf)
    print(eda_formula.cnf)
