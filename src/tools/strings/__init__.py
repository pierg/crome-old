import hashlib
import random
import re
import string
from typing import Tuple, List

from controller.synthesisinfo import SynthesisInfo
from tools.logic import Logic


class StringMng:
    ASSUMPTIONS_HEADER = '**ASSUMPTIONS**'
    GUARANTEES_HEADER = '**GUARANTEES**'
    INS_HEADER = '**INPUTS**'
    OUTS_HEADER = '**OUTPUTS**'
    END_HEADER = '**END**'
    HEADER_SYMBOL = '**'
    DATA_INDENT = 0

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
            res = re.sub(r'!(?!\s)', '! ', text)
            res = res.replace("TRUE", "true")
        except Exception as e:
            raise e
        return res

    @staticmethod
    def get_controller_synthesis_str(controller_info: SynthesisInfo) -> str:

        ret = ""

        if len(controller_info.assumptions) > 0:
            ret += f"{StringMng.ASSUMPTIONS_HEADER}\n\n"
            for p in controller_info.assumptions:
                ret += "\t" * StringMng.DATA_INDENT + StringMng.strix_syntax_fix(p) + "\n"

        if len(controller_info.a_liveness) > 0:
            for p in controller_info.a_liveness:
                ret += "\t" * StringMng.DATA_INDENT + StringMng.strix_syntax_fix(p) + "\n"

        if len(controller_info.a_mutex) > 0:
            for p in controller_info.a_mutex:
                ret += "\t" * StringMng.DATA_INDENT + StringMng.strix_syntax_fix(p) + "\n"

        ret += f"\n\n{StringMng.GUARANTEES_HEADER}\n\n"
        for p in controller_info.guarantees:
            ret += "\t" * StringMng.DATA_INDENT + StringMng.strix_syntax_fix(p) + "\n"

        if len(controller_info.g_mutex) > 0:
            for p in controller_info.g_mutex:
                ret += "\t" * StringMng.DATA_INDENT + StringMng.strix_syntax_fix(p) + "\n"

        if len(controller_info.g_adjacency) > 0:
            for p in controller_info.g_adjacency:
                ret += "\t" * StringMng.DATA_INDENT + StringMng.strix_syntax_fix(p) + "\n"

        ret += f"\n\n{StringMng.INS_HEADER}\n\n"
        ret += "\t" * StringMng.DATA_INDENT + ", ".join(controller_info.inputs)

        ret += f"\n\n{StringMng.OUTS_HEADER}\n\n"
        ret += "\t" * StringMng.DATA_INDENT + ", ".join(controller_info.outputs)

        ret += f"\n\n{StringMng.END_HEADER}\n\n"

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

        assumptions = []
        guarantees = []
        inputs = []
        outputs = []

        file_header = ""

        with open(file_path, 'r') as ifile:
            for line in ifile:
                line, header = StringMng._check_header(line)

                # skip empty lines
                if not line:
                    continue

                # parse file header line
                elif header:

                    if StringMng.ASSUMPTIONS_HEADER == line:
                        if file_header == "":
                            file_header = line
                        else:
                            Exception("File format not supported")

                    elif StringMng.GUARANTEES_HEADER == line:
                        if file_header == StringMng.ASSUMPTIONS_HEADER:
                            file_header = line
                        else:
                            Exception("File format not supported")

                    elif StringMng.INS_HEADER == line:
                        if file_header == StringMng.GUARANTEES_HEADER:
                            file_header = line
                        else:
                            Exception("File format not supported")

                    elif StringMng.OUTS_HEADER == line:
                        if file_header == StringMng.INS_HEADER:
                            file_header = line
                        else:
                            Exception("File format not supported")

                    elif StringMng.END_HEADER == line:
                        if file_header == StringMng.OUTS_HEADER:
                            if len(assumptions) == 0:
                                assumptions.append("true")
                            return Logic.and_(assumptions), Logic.and_(guarantees), ",".join(inputs), ",".join(outputs)
                        else:
                            Exception("File format not supported")
                    else:
                        raise Exception("Unexpected File Header: " + line)

                else:

                    if StringMng.ASSUMPTIONS_HEADER == file_header:
                        assumptions.append(line.strip())

                    if StringMng.GUARANTEES_HEADER == file_header:
                        guarantees.append(line.strip())

                    if StringMng.INS_HEADER == file_header:
                        inputs.append(line.strip())

                    if StringMng.OUTS_HEADER == file_header:
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

    @staticmethod
    def _check_header(line: str) -> Tuple[str, bool]:
        """Returns a comment-free, tab-replaced line with no whitespace and the number of tabs"""
        COMMENT_CHAR = '#'
        line = line.split(COMMENT_CHAR, 1)[0]
        if line.startswith(StringMng.HEADER_SYMBOL):
            return line.strip(), True
        return line.strip(), False
