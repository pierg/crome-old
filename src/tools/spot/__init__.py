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
    f_string = "p -> (G(a & b | F c ) & !(a | x U d) | (c & a) & !(F c | d) | a & b) & (c | d) & (c | d) & (c | d) & (c | d) & (c | d) | a U b & F g | G x"

    f = spot.formula(f_string)

    print("\n\n\\_____________*******______________")
    f1 = f
    print(f1)

    # kindstar() prints the name of the operator
    # size() return the number of operands of the operators
    print(f"{f1.kindstr()}, {f1.size()} children")
    # [] accesses each operand
    print("left: {f[0]}, right: {f[1]}".format(f=f1))
    # you can also iterate over all operands using a for loop
    for child in f1:
        print("  *", child)

    print("\n\n\\_____________*******______________")
    f2 = spot.negative_normal_form(f)
    print(f2)

    # kindstar() prints the name of the operator
    # size() return the number of operands of the operators
    print(f"{f2.kindstr()}, {f2.size()} children")
    # [] accesses each operand
    print("left: {f[0]}, right: {f[1]}".format(f=f2))
    # you can also iterate over all operands using a for loop
    for child in f2:
        print("  *", child)

    print("\n\n\\_____________*******______________")
    f3 = spot.simplify(f)
    print(f3)

    # kindstar() prints the name of the operator
    # size() return the number of operands of the operators
    print(f"{f3.kindstr()}, {f3.size()} children")
    # [] accesses each operand
    print("left: {f[0]}, right: {f[1]}".format(f=f3))
    # you can also iterate over all operands using a for loop
    for child in f3:
        print("  *", child)
