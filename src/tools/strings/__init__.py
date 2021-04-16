import hashlib
import random
import re
import string
from typing import Tuple, List

from controller.synthesisinfo import SynthesisInfo
from tools.logic import Logic


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
            for p in controller_info.a_liveness:
                ret += "\t" + StringMng.strix_syntax_fix(p) + "\n"

        if len(controller_info.a_mutex) > 0:
            for p in controller_info.a_mutex:
                ret += "\t" + StringMng.strix_syntax_fix(p) + "\n"

        ret += "\n\nGUARANTEES\n\n"
        for p in controller_info.guarantees:
            ret += "\t" + StringMng.strix_syntax_fix(p) + "\n"

        if len(controller_info.g_mutex) > 0:
            for p in controller_info.g_mutex:
                ret += "\t" + StringMng.strix_syntax_fix(p) + "\n"

        if len(controller_info.g_adjacency) > 0:
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

    @staticmethod
    def parse_controller_specification_from_file(file_path: str) -> Tuple[str, str, str, str]:
        """Returns: assumptions, guarantees, inputs, outputs"""

        ASSUMPTIONS_HEADER = 'ASSUMPTIONS'
        GUARANTEES_HEADER = 'GUARANTEES'
        INS_HEADER = 'INPUTS'
        OUTS_HEADER = 'OUTPUTS'
        END_HEADER = 'END'
        FILE_HEADER_INDENT = 0
        DATA_INDENT = 1

        assumptions = []
        guarantees = []
        inputs = []
        outputs = []

        file_header = ""

        with open(file_path, 'r') as ifile:
            for line in ifile:
                line, ntabs = StringMng._count_line(line)

                # skip empty lines
                if not line:
                    continue

                # parse file header line
                elif ntabs == FILE_HEADER_INDENT:

                    if ASSUMPTIONS_HEADER == line:
                        if file_header == "":
                            file_header = line
                        else:
                            Exception("File format not supported")

                    elif GUARANTEES_HEADER == line:
                        if file_header == ASSUMPTIONS_HEADER:
                            file_header = line
                        else:
                            Exception("File format not supported")

                    elif INS_HEADER == line:
                        if file_header == GUARANTEES_HEADER:
                            file_header = line
                        else:
                            Exception("File format not supported")

                    elif OUTS_HEADER == line:
                        if file_header == INS_HEADER:
                            file_header = line
                        else:
                            Exception("File format not supported")

                    elif END_HEADER == line:
                        if file_header == OUTS_HEADER:
                            if len(assumptions) == 0:
                                assumptions.append("true")
                            return Logic.and_(assumptions), Logic.and_(guarantees), ",".join(inputs), ",".join(outputs)
                        else:
                            Exception("File format not supported")
                    else:
                        raise Exception("Unexpected File Header: " + line)

                else:

                    if ASSUMPTIONS_HEADER == file_header:
                        if ntabs == DATA_INDENT:
                            assumptions.append(line.strip())

                    if GUARANTEES_HEADER == file_header:
                        if ntabs == DATA_INDENT:
                            guarantees.append(line.strip())

                    if INS_HEADER == file_header:
                        if ntabs == DATA_INDENT:
                            inputs.append(line.strip())

                    if OUTS_HEADER == file_header:
                        if ntabs == DATA_INDENT:
                            outputs.append(line.strip())

    @staticmethod
    def _count_line(line):
        """Returns a comment-free, tab-replaced line with no whitespace and the number of tabs"""
        COMMENT_CHAR = '#'
        TAB_WIDTH = 2
        line = line.split(COMMENT_CHAR, 1)[0]  # remove comments
        tab_count = 0
        space_count = 0
        for char in line:
            if char == ' ':
                space_count += 1
            elif char == '\t':
                tab_count += 1
            else:
                break
        tab_count += int(space_count / 4)
        line = line.replace('\t', ' ' * TAB_WIDTH)  # replace tabs with spaces
        return line.strip(), tab_count
