import os

from tools.persistence import Persistence

output_folder_path = (
    f"{Persistence.default_folder_path}/examples/{os.path.basename(os.getcwd())}"
)


"""Load CGG"""
cgg = Persistence.load_cgg(output_folder_path)

"""Realize Specification and Transition Controllers indicating the Maximum Transition Time"""
cgg.realize_all(t_trans=3)
print(cgg)

"""Save CGG again with the controllers information"""
cgg.save()

"""Save CGG for persistence"""
Persistence.dump_cgg(cgg)
