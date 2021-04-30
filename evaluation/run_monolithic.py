import os, sys
from controller import Controller
from tools.storage import Store
from tools.strings import StringMng
from tools.strix import Strix
from specification.atom.pattern.robotics.trigger.triggers_modified import *
from worlds.illustrative_example import RunningExample

w = RunningExample()
greet = BoundReaction(w["person"], w["greet"], w["active"], w["day"])
register = BoundDelay(w["person"], w["register"], w["active"], w["day"])
print(greet)
print(register)

path = os.path.abspath(os.path.dirname(__file__))

controller_name = "spec"

print(f"controller selected: {path}/{controller_name}.txt")

a, g, i, o = StringMng.parse_controller_specification_from_file(f"{path}/{controller_name}.txt")
realizable, kiss_format, exec_time = Strix.generate_controller(a, g, i, o)

res = f"TIME MONOLITHIC SYNTHESIS    \t= {exec_time}\n\n"
Store.save_to_file(res, f"monolithic_time.txt", absolute_folder_path=f"{path}")

controller = Controller(mealy_machine=kiss_format, synth_time=exec_time)

print("\n~~~MEALY MACHINE~~~\n" + str(controller))
Store.save_to_file(str(controller), f"{controller_name}_table.txt", absolute_folder_path=f"{path}")

run = controller.simulate()
print("\n\n\n~~~SIMULATION OF A RUN~~~\n" + run)
Store.save_to_file(str(run), f"{controller_name}_run.txt", absolute_folder_path=f"{path}")
