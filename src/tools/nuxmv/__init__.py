import subprocess
from typing import List, Tuple

from tools.logic import Logic
from type import Boolean, BoundedInteger
from typeset import Typeset

smvfile = "nusmvfile.smv"


class Nuxmv:

    @staticmethod
    def __convert_to_nuxmv(typeset: Typeset) -> List[str]:
        tuple_vars = []
        for k, v in typeset.items():
            if isinstance(v, Boolean):
                tuple_vars.append(f"{k}: boolean")
            elif isinstance(v, BoundedInteger):
                tuple_vars.append(f"{k}: {k.min}..{k.max}")
        return tuple_vars

    @staticmethod
    def check_satisfiability(formula: Tuple[str, Typeset]) -> bool:

        expression, typeset = formula

        if not isinstance(expression, str) or not isinstance(typeset, Typeset):
            raise AttributeError

        if expression == "TRUE":
            return True

        if expression == "FALSE":
            return False

        variables = Nuxmv.__convert_to_nuxmv(typeset)

        """Write the NuSMV file"""
        with open(smvfile, 'w') as ofile:

            ofile.write('MODULE main\n')

            ofile.write('VAR\n')

            for v in list(set(variables)):
                ofile.write(f"\t{v};\n")

            ofile.write('\n')
            ofile.write('LTLSPEC ')
            ofile.write(str(Logic.not_(expression)))

            ofile.write('\n')

        try:
            output = subprocess.check_output(['nuXmv', smvfile], encoding='UTF-8',
                                             stderr=subprocess.DEVNULL).splitlines()
            output = [x for x in output if not (x[:3] == '***' or x[:7] == 'WARNING' or x == '')]
            for line in output:
                if line[:16] == '-- specification':
                    if 'is false' in line:
                        print("\t\t\tSAT-YES:\t" + str(expression))
                        return True
                    elif 'is true' in line:
                        print("\t\t\tSAT-NO :\t" + str(expression))
                        return False

        except Exception as e:
            with open(smvfile, 'r') as fin:
                print(fin.read())
            raise e

    @staticmethod
    def check_validity(formula: Tuple[str, Typeset]) -> bool:

        expression, typeset = formula

        if not isinstance(expression, str) or not isinstance(typeset, Typeset):
            raise AttributeError

        if expression == "TRUE":
            return True

        if expression == "FALSE":
            return False

        variables = Nuxmv.__convert_to_nuxmv(typeset)

        """Write the NuSMV file"""
        with open(smvfile, 'w') as ofile:

            ofile.write('MODULE main\n')

            ofile.write('VAR\n')

            for v in list(set(variables)):
                ofile.write('\t' + v + ";\n")

            ofile.write('\n')
            ofile.write('LTLSPEC ' + expression)

        try:
            output = subprocess.check_output(['nuXmv', smvfile], encoding='UTF-8',
                                             stderr=subprocess.DEVNULL).splitlines()
            output = [x for x in output if not (x[:3] == '***' or x[:7] == 'WARNING' or x == '')]
            for line in output:
                if line[:16] == '-- specification':
                    if 'is false' in line:
                        print("\t\t\tVAL-NO :\t" + expression)
                        return False
                    elif 'is true' in line:
                        print("\t\t\tVAL-YES:\t" + expression)
                        return True

        except Exception as e:
            with open(smvfile, 'r') as fin:
                print(fin.read())
            raise e
