import os

from tests.synthesis_examples import folder_name
from tools.persistence import Persistence


path = os.path.abspath(os.path.dirname(__file__))


controller = Persistence.load_controller(path)

run = controller.simulate()
print(run)

