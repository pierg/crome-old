import subprocess
import platform
from typing import Tuple

from tools.logic import Logic

import time
import docker

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

        global command, timeout

        """Fix syntax"""
        assumptions = StringMng.strix_syntax_fix(assumptions)
        guarantees = StringMng.strix_syntax_fix(guarantees)

        print("\n\n")
        print(assumptions)
        print("\n")
        print(guarantees)
        print("\n")
        print(ins)
        print("\n")
        print(outs)
        print("\n\n")

        try:
            if ins == "":
                strix_specs = f"-f '{Logic.implies_(assumptions, guarantees)}' --outs='{outs}'"
            else:
                strix_specs = f"-f '{Logic.implies_(assumptions, guarantees)}' --ins='{ins}' --outs='{outs}'"

            strix_bin = "strix "
            docker_image = "pmallozzi/ltltools"

            if kiss:
                """Kiss format"""
                command = f"{strix_bin} --kiss {strix_specs}"
            else:
                """Dot format"""
                command = f"{strix_bin} --dot {strix_specs}"

            timeout = 3600
            print("\n\nRUNNING COMMAND:\n\n" + command + "\n\n")
            start_time = time.time()

            if platform.system() != "Linux":
                client = docker.from_env()
                result = str(client.containers.run(image=docker_image,
                                                    command=command,
                                                    remove=True)).split("\\n")
                result.pop()
                result[0] = result[0][2:]
            else:
                result = subprocess.check_output([command], shell=True, timeout=timeout, encoding='UTF-8').splitlines()

        except subprocess.TimeoutExpired:
            raise SynthesisTimeout(command=command, timeout=timeout)
        except Exception as e:
            raise UnknownStrixResponse(command=command, response=e.output)

        exec_time = time.time() - start_time

        if "REALIZABLE" in result:
            realizable = True
        elif "UNREALIZABLE" in result:
            realizable = False
        else:
            raise UnknownStrixResponse(command=command, response="\n".join(result))

        processed_return = ""

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
