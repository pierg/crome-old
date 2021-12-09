import os

from core.cgg import Node
from core.cgg.exceptions import CGGException
from tools.persistence import Persistence

output_folder_path = (
    f"{Persistence.default_folder_path}/examples/{os.path.basename(os.getcwd())}"
)

try:

    """Load the goals."""
    set_of_goals = Persistence.load_goals(output_folder_path)

    """Automatically build the CGG"""
    cgg = Node.build_cgg(set_of_goals)
    print(cgg)

    """Setting the saving folder"""
    cgg.set_session_name(f"examples/{os.path.basename(os.getcwd())}")
    """Save CGG as text file"""
    cgg.save()
    """Save CGG so that it can be loaded later"""
    Persistence.dump_cgg(cgg, output_folder_path)


except CGGException as e:
    raise e
