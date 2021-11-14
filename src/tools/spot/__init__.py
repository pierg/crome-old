import platform
import subprocess

import spot

from tools.storage import Store


class Spot:
    @staticmethod
    def generate_buchi(specification: str, name: str, path: str = None):
        try:

            print(f"Generating Buchi for...\n{specification}")

            if platform.system() != "Linux":
                command = (
                    f"docker run pmallozzi/ltltools ltl2tgba -B {specification} -d"
                )
                result = subprocess.check_output(
                    [command], shell=True, encoding="UTF-8", stderr=subprocess.DEVNULL
                ).splitlines()
            else:
                result = subprocess.check_output(
                    ["ltl2tgba", "-B", specification, "-d"],
                    encoding="UTF-8",
                    stderr=subprocess.DEVNULL,
                ).splitlines()

            result = [x for x in result if not ("[Büchi]" in x)]
            result = "".join(result)

            Store.save_to_file(specification, f"{name}_specs.txt", path)
            Store.save_to_file(result, f"{name}_dot.txt", path)
            Store.generate_eps_from_dot(result, name, path)

            print(f"Buchi generated")

        except Exception as e:
            raise e


if __name__ == "__main__":

    # f = spot.formula("((G(F(r1 & F(r2))) & (!(r2) U r1) & (!(r2) U r1) & G(((r2) -> (X((!(r2) U r1))))) & G(((r1) -> (X((!(r1) U r2)))))) | !(GF(sensor))) & (F(a) | GF(b))")
    f_string = "p -> ((a & b | c ) & (a | d) | (c & a) & (c | d) | a & b) & (c | d) & (c | d) & (c | d) & (c | d) & (c | d)"
    f = spot.formula(f_string)
    f2 = spot.negative_normal_form(f)
    f3 = spot.simplify(f)
    print(f_string)
    print(f)
    print(f2)

    print(f3)
