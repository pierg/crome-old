import os

from casestudies.find_and_repair_specifications.goals import set_of_goals
from core.cgg import Node
from tools.persistence import Persistence

output_folder_path = (
    f"{Persistence.default_folder_path}/casestudies/{os.path.basename(os.getcwd())}"
)


cgg = Node.build_cgg(set_of_goals)
print(cgg)

"""Setting the saving folder"""
cgg.set_session_name(f"examples/{os.path.basename(os.getcwd())}")
"""Save CGG as text file"""
cgg.save()
"""Save CGG so that it can be loaded later"""
# Persistence.dump_cgg(cgg, output_folder_path)
