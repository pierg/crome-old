import os

from controller import Controller
from tools.persistence import Persistence
from tools.storage import Store
from tools.strings import StringMng
from tools.strix import Strix


path = os.path.abspath(os.path.dirname(__file__))

controller_name = "good_0"

a, g, i, o = StringMng.parse_controller_specification_from_file(f"{path}/{controller_name}.txt")
realizable, kiss_format, exec_time = Strix.generate_controller(a, g, i, o)
controller = Controller(mealy_machine=kiss_format)


Persistence.dump_controller(controller, path, controller_name)

print(controller)
Store.save_to_file(str(controller), f"{controller_name}_table.txt", absolute_folder_path=f"{path}")

run = controller.simulate()
print(run)
Store.save_to_file(str(run), f"{controller_name}_run.txt", absolute_folder_path=f"{path}")

