import os

from controller import Controller
from tests.synthesis_examples import folder_name
from tools.persistence import Persistence
from tools.strings import StringMng
from worlds.illustrative_example import IllustrativeExample

world = IllustrativeExample()

path = os.path.abspath(os.path.dirname(__file__))

a, g, i, o = StringMng.parse_controller_specification_from_file(f"{path}/controller_specs.txt")
realizable, dot_format, kiss_format, exec_time = Controller.generate_controller(a, g, i, o)
controller = Controller(mealy_machine=kiss_format, world=world)

print("\n\nCONTROLLER:")
print(controller)

Persistence.dump_controller(controller, path)
