import os
from core.controller import Controller
from running_example.modeling_environment import RunningExample
from tools.persistence import Persistence
from tools.storage import Store
from tools.strings import StringMng
from tools.strix import Strix
from core.specification.atom.pattern.robotics.trigger.triggers_modified import *


path = os.path.abspath(os.path.dirname(__file__))

controller_name = "spec_simple"

controller = Persistence.load_controller(f"{path}", name=f"{controller_name}")

run = controller.simulate_day_night()
print("\n\n\n~~~SIMULATION OF A RUN~~~\n" + run)
Store.save_to_file(str(run), f"{controller_name}_run.txt", absolute_folder_path=f"{path}")
