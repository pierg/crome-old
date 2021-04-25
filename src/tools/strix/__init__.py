import subprocess
import platform
from typing import Tuple

from tools.logic import Logic

import time

from tools.strings import StringMng
from tools.strix.exceptions import *


class Strix:

    @staticmethod
    def generate_controller(assumptions: str,
                            guarantees: str,
                            ins: str,
                            outs: str,
                            kiss: bool = True) -> Tuple[bool, str, float]:
        """It returns:
            bool: indicating if a contorller has been synthetised
            str: mealy machine of the controller (if found) or of the counter-examples if not found in dot format
            float: indicating the controller time"""

        global command_dot, timeout

        """Fix syntax"""
        assumptions = StringMng.strix_syntax_fix(assumptions)
        guarantees = StringMng.strix_syntax_fix(guarantees)

        try:
            if ins == "":
                strix_specs = Logic.implies_(assumptions, guarantees) + '" --outs="' + outs + '"'
            else:
                strix_specs = Logic.implies_(assumptions, guarantees) + '" --ins="' + ins + '" --outs="' + outs + '"'

            if platform.system() != "Linux":
                strix_bin = "docker run lazkany/strix "
            else:
                strix_bin = "strix "

            if kiss:
                """Kiss format"""
                command = f"{strix_bin} --kiss -f {strix_specs}"
            else:
                """Dot format"""
                command = f"{strix_bin} --dot -f {strix_specs}"

            timeout = 3600
            print("\n\nRUNNING COMMAND:\n\n" + command + "\n\n")
            start_time = time.time()
            result = subprocess.check_output([command], shell=True, timeout=timeout,
                                                  encoding='UTF-8').splitlines()

        except subprocess.TimeoutExpired:
            raise SynthesisTimeout(command=command_dot, timeout=timeout)
        except Exception as e:
            raise UnknownStrixResponse(command=command_dot, response=e.__str__())

        exec_time = time.time() - start_time

        if "REALIZABLE" in result:
            realizable = True
        elif "UNREALIZABLE" in result:
            realizable = False
        else:
            raise UnknownStrixResponse(command=command_dot, response="\n".join(result))

        if kiss:
            for i, line in enumerate(result):
                if ".inputs" not in line:
                    continue
                else:
                    processed_return = "\n".join(result[i:])
                    break
        else:
            for i, line in enumerate(result):
                if "digraph" not in line:
                    continue
                else:
                    processed_return = "".join(result[i:])
                    break

        return realizable, processed_return, exec_time
