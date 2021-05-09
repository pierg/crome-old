import os
from controller import Controller
from running_example.modeling_environment import RunningExample
from tools.persistence import Persistence
from tools.storage import Store
from tools.strings import StringMng
from tools.strix import Strix
from specification.atom.pattern.robotics.trigger.triggers_modified import *


path = os.path.abspath(os.path.dirname(__file__))

controller_name = "spec"

print(f"controller selected: {path}/{controller_name}.txt")

a, g, i, o = StringMng.parse_controller_specification_from_file(f"{path}/{controller_name}.txt")
realizable, kiss_format, exec_time = Strix.generate_controller(a, g, i, o)

controller = Controller(mealy_machine=kiss_format, synth_time=exec_time)


res = f"TIME MONOLITHIC SYNTHESIS    \t= {exec_time}\nN OF STATES:\t{len(controller.states)}\nN OF EDGES:\t{len(controller.transitions)}"
Store.save_to_file(res, f"monolithic_time.txt", absolute_folder_path=f"{path}")

Persistence.dump_controller(controller, f"{path}", name=f"{controller_name}")

print("\n~~~MEALY MACHINE~~~\n" + str(controller))
Store.save_to_file(str(controller), f"{controller_name}_table.txt", absolute_folder_path=f"{path}")

run = controller.simulate_day_night()
print("\n\n\n~~~SIMULATION OF A RUN~~~\n" + run)
Store.save_to_file(str(run), f"{controller_name}_run.txt", absolute_folder_path=f"{path}")

print(f"\n\nRESULTS:\n{res}")