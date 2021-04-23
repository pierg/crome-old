import os, sys

from tools.persistence import Persistence

path = os.path.abspath(os.path.dirname(__file__))


controller_name = sys.argv[0]

controller = Persistence.load_controller(folder_path=path, name=controller_name)

print(controller)
run = controller.simulate()
print(run)

