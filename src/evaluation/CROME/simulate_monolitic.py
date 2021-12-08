import os

from tools.persistence import Persistence
from tools.storage import Store

path = os.path.abspath(os.path.dirname(__file__))

controller_name = "spec_simple"

controller = Persistence.load_controller(f"{path}", name=f"{controller_name}")

run = controller.simulate_day_night()
print("\n\n\n~~~SIMULATION OF A RUN~~~\n" + run)
Store.save_to_file(
    str(run), f"{controller_name}_run.txt", absolute_folder_path=f"{path}"
)
