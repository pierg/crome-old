from core.specification.legacy.formula import FormulaOutput


def pretty_print(self, formulatype: FormulaOutput = FormulaOutput.CNF):
    return self.formula(formulatype)[0]
