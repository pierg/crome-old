import os

from tools.persistence import Persistence

path = os.path.abspath(os.path.dirname(__file__))


controller = Persistence.load_controller(path)

print(controller)
run = controller.simulate()
print(run)
