import subprocess
import platform

from tools.logic import Logic

import time

from tools.strix.exceptions import *


class Strix:

    @staticmethod
    def generate_controller(assumptions: str, guarantees: str, ins: str, outs: str) -> Tuple[bool, str, str, float]:
        """It returns:
            bool: indicating if a contorller has been synthetised
            str: mealy machine of the controller (if found) or of the counter-examples if not found in dot format
            float: indicating the controller time"""

        global command_dot, timeout
        try:
            if ins == "":
                strix_specs = Logic.implies_(assumptions, guarantees) + '" --outs="' + outs + '"'
            else:
                strix_specs = Logic.implies_(assumptions, guarantees) + '" --ins="' + ins + '" --outs="' + outs + '"'
            command_dot = ""
            if platform.system() != "Linux":
                docker_command = 'docker run lazkany/strix'
                docker_params_dot = ' -f "' + strix_specs + " --k --dot"
                docker_params_kiss = ' -f "' + strix_specs + " --kiss"
                command_dot = docker_command + docker_params_dot
                command_kiss = docker_command + docker_params_kiss
            else:
                params_dot = ' -k --dot -f "' + strix_specs
                params_kiss = ' -k --kiss -f "' + strix_specs
                command_dot = "strix" + params_dot
                command_kiss = "strix" + params_kiss
            timeout = 3600
            print("\n\nRUNNING COMMAND:\n\n" + command_dot + "\n\n")
            start_time = time.time()
            result_dot = subprocess.check_output([command_dot], shell=True, timeout=timeout, encoding='UTF-8').split()
            result_kiss = subprocess.check_output([command_kiss], shell=True, timeout=timeout,
                                                  encoding='UTF-8').splitlines()

        except subprocess.TimeoutExpired:
            raise SynthesisTimeout(command=command_dot, timeout=timeout)
        except Exception as e:
            raise UnknownStrixResponse(command=command_dot, response=e.__str__())

        exec_time = time.time() - start_time
        dot_format = ""
        kiss_format = ""
        if "REALIZABLE" in result_dot:
            realizable = True
        elif "UNREALIZABLE" in result_dot:
            realizable = False
        else:
            raise UnknownStrixResponse(command=command_dot, response="\n".join(result_dot))
        for i, line in enumerate(result_dot):
            if "digraph" not in line:
                continue
            else:
                dot_format = "".join(result_dot[i:])
                break
        for i, line in enumerate(result_kiss):
            if ".inputs" not in line:
                continue
            else:
                kiss_format = "\n".join(result_kiss[i:])
                break
        return realizable, dot_format, kiss_format, exec_time
