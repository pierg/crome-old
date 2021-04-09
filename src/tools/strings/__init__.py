import hashlib
import random
import re
import string
from typing import Tuple, List

from controller.synthesisinfo import SynthesisInfo


class StringMng:

    @staticmethod
    def get_name_and_id(value: str = None) -> Tuple[str, str]:

        if value is None:
            name: str = ""

            """5 character ID generated from a random string"""
            random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            id = hashlib.sha1(random_string.encode("UTF-8")).hexdigest()[:5]
        else:
            name: str = value

            """5 character ID generated from the name"""
            id: str = hashlib.sha1(value.encode("UTF-8")).hexdigest()[:5]

        return name, id

    @staticmethod
    def strix_syntax_fix(text: str):
        """Adds a space next to the '!' and converts TRUE to true"""
        try:
            res = re.sub(r'(!)', '! ', text)
            res = res.replace("TRUE", "true")
        except Exception as e:
            raise e
        return res

    @staticmethod
    def get_controller_synthesis_str(controller_info: SynthesisInfo) -> str:

        ret = ""

        if len(controller_info.assumptions) > 0:
            ret += "ASSUMPTIONS\n\n"
            for p in controller_info.assumptions:
                ret += "\t" + StringMng.strix_syntax_fix(p) + "\n"

        if len(controller_info.a_liveness) > 0:
            ret += "\n\nASSUMPTIONS_LIVENESS\n\n"
            for p in controller_info.a_liveness:
                ret += "\t" + StringMng.strix_syntax_fix(p) + "\n"

        if len(controller_info.a_mutex) > 0:
            ret += "\n\nASSUMPTIONS_MUTEX\n\n"
            for p in controller_info.a_mutex:
                ret += "\t" + StringMng.strix_syntax_fix(p) + "\n"

        ret += "\n\nGUARANTEES\n\n"
        for p in controller_info.guarantees:
            ret += "\t" + StringMng.strix_syntax_fix(p) + "\n"

        if len(controller_info.g_mutex) > 0:
            ret += "\n\nGUARANTEES_MUTEX\n\n"
            for p in controller_info.g_mutex:
                ret += "\t" + StringMng.strix_syntax_fix(p) + "\n"

        if len(controller_info.g_adjacency) > 0:
            ret += "\n\nGUARANTEES_ADJACENCY\n\n"
            for p in controller_info.g_adjacency:
                ret += "\t" + StringMng.strix_syntax_fix(p) + "\n"

        ret += "\n\nINPUTS\n\n"
        ret += "\t" + ", ".join(controller_info.inputs)

        ret += "\n\nOUTPUTS\n\n"
        ret += "\t" + ", ".join(controller_info.outputs)

        ret += "\n\nEND\n\n"

        return ret

    @staticmethod
    def get_inputs_from_kiss(text: str) -> List[str]:
        inputsline = text.splitlines()[0]
        return inputsline.split()[1:]

    @staticmethod
    def get_outputs_from_kiss(text: str) -> List[str]:
        outputsline = text.splitlines()[1]
        return outputsline.split()[1:]

    @staticmethod
    def get_states_from_kiss(text: str) -> List[str]:
        states = []
        statesline = text.splitlines()[5]
        state_n = int(statesline.split()[1])
        for i in range(state_n):
            states.append(f"S{i}")
        return states

    @staticmethod
    def get_initial_state_from_kiss(text: str) -> str:
        initialstateline = text.splitlines()[6]
        return initialstateline.split()[1]
