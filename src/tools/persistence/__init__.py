import os
import pickle
from cgg import Node


class Persistence:
    output_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'output'))

    @staticmethod
    def dump_cgg(cgg: Node):

        if cgg.session_name is not None:
            output_folder = f"{Persistence.output_folder}/{cgg.session_name}"
        else:
            output_folder = f"{Persistence.output_folder}"

        output_file = f"{output_folder}/cgg.dat"

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        file = open(output_file, 'wb')
        pickle.dump(cgg, file)
        file.close()


    @staticmethod
    def load_cgg(session_folder_name: str) -> Node:

        if session_folder_name is not None:
            output_folder = f"{Persistence.output_folder}/{session_folder_name}"
        else:
            output_folder = f"{Persistence.output_folder}"

        file = f"{output_folder}/cgg.dat"

        file = open(file, 'rb')
        cgg = pickle.load(file)
        file.close()

        return cgg
