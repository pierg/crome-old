import os
import subprocess
from enum import Enum
from typing import List, Tuple
from pathlib import Path
import docker
from tools.logic import Logic
from core.type import Boolean, BoundedInteger
from core.typeset import Typeset


class CheckType(Enum):
    SATISFIABILITY = 0
    VALIDITY = 1


class Nuxmv:
    output_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'output'))
    nusmvfilename = "nusmvfile.smv"
    output_file = f"{output_folder}/{nusmvfilename}"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    folder_path = Path(output_folder)
    file_path = Path(output_file)

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
    def __write_file(variables: List[str], expression: str, check_type: CheckType):
        with open(Nuxmv.file_path, 'w') as ofile:
            ofile.write('MODULE main\n')
            ofile.write('VAR\n')
            for v in list(set(variables)):
                ofile.write(f"\t{v};\n")
            ofile.write('\n')
            ofile.write('LTLSPEC ')
            if check_type.SATISFIABILITY:
                ofile.write(str(Logic.not_(expression)))
            elif check_type.VALIDITY:
                ofile.write('LTLSPEC ' + expression)
            else:
                raise Exception("Type of checking not supported")
            ofile.write('\n')

    @staticmethod
    def __parse_output(output: List[str], check_type: CheckType) -> bool:
        for line in output:
            if line[:16] == '-- specification':
                spec = line[16:].partition("is")[0]
                if 'is false' in line:
                    if check_type == CheckType.SATISFIABILITY:
                        print("\t\t\tSAT-YES:\t" + spec)
                        return True
                    elif check_type == CheckType.VALIDITY:
                        print("\t\t\tVAL-NO :\t" + spec)
                        return False
                    else:
                        raise Exception("Type of checking not supported")
                elif 'is true' in line:
                    if check_type == CheckType.SATISFIABILITY:
                        print("\t\t\tSAT-NO :\t" + spec)
                        return False
                    elif check_type == CheckType.VALIDITY:
                        print("\t\t\tVAL-YES:\t" + spec)
                        return True
                    else:
                        raise Exception("Type of checking not supported")
                else:
                    raise Exception("nuXmv produced something unexpected")

    @staticmethod
    def __trivialchecks(expression: str):
        if expression == "TRUE":
            return True

        if expression == "FALSE":
            return False

    @staticmethod
    def __launch_nuxmv() -> List[str]:
        try:
            """"Trying nuXmv locally"""
            output = subprocess.check_output(['nuXmv', Nuxmv.file_path], encoding='UTF-8',
                                             stderr=subprocess.DEVNULL).splitlines()



        except Exception as e:
            """"Trying nuXmv with docker"""
            docker_image = "pmallozzi/ltltools"
            client = docker.from_env()
            output = str(client.containers.run(image=docker_image,
                                               volumes={f"{Nuxmv.folder_path}": {'bind': '/home/',
                                                                                 'mode': 'rw'}},
                                               command=f"nuXmv /home/{Nuxmv.nusmvfilename}",
                                               remove=True)).split("\\n")

        output = [x for x in output if not (x[:3] == '***' or x[:7] == 'WARNING' or x == '')]
        return output

    @staticmethod
    def check_satisfiability(formula: Tuple[str, Typeset]) -> bool:

        expression, typeset = formula

        if not isinstance(expression, str) or not isinstance(typeset, Typeset):
            raise AttributeError

        Nuxmv.__trivialchecks(expression)

        variables = Nuxmv.__convert_to_nuxmv(typeset)

        Nuxmv.__write_file(variables, expression, CheckType.SATISFIABILITY)

        output = Nuxmv.__launch_nuxmv()

        return Nuxmv.__parse_output(output, CheckType.SATISFIABILITY)

    @staticmethod
    def check_validity(formula: Tuple[str, Typeset]) -> bool:

        expression, typeset = formula

        Nuxmv.__trivialchecks(expression)

        variables = Nuxmv.__convert_to_nuxmv(typeset)

        Nuxmv.__write_file(variables, expression, CheckType.VALIDITY)

        output = Nuxmv.__launch_nuxmv()

        return Nuxmv.__parse_output(output, CheckType.VALIDITY)
