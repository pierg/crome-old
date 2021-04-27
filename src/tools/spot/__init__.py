import subprocess
from tools.storage import Store
import platform

class Spot:

    @staticmethod
    def generate_buchi(specification: str, name: str, path: str = None):
        try:

            print(f"Generating Buchi for...\n{specification}")


            if platform.system() != "Linux":
                command = f"docker run pmallozzi/ltltools ltl2tgba -B {specification} -d"
                result = subprocess.check_output([command], shell=True, encoding='UTF-8',
                                                 stderr=subprocess.DEVNULL).splitlines()
            else:
                result = subprocess.check_output(["ltl2tgba", "-B", specification, "-d"], encoding='UTF-8',
                                                 stderr=subprocess.DEVNULL).splitlines()



            result = [x for x in result if not ('[Büchi]' in x)]
            result = "".join(result)

            Store.save_to_file(specification, f"{name}_specs.txt", path)
            Store.save_to_file(result, f"{name}_dot.txt", path)
            Store.generate_eps_from_dot(result, name, path)

            print(f"Buchi generated")


        except Exception as e:
            raise e
