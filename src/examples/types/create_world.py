from core.specification.exceptions import NotSatisfiableException
from core.world import World
from examples.types.create_types import (
    R1,
    R2,
    R3,
    R4,
    R5,
    Day,
    Greet,
    Movement,
    Night,
    Person,
    Picture,
    Register,
)


class CustomWorld(World):
    def __init__(self):
        super().__init__(
            actions={Picture(), Greet(), Register()},
            locations={R1(), R2(), R3(), R4(), R5()},
            sensors={Movement(), Person()},
            contexts={Day(), Night()},
        )


"""Create the world, i.e. a dictionary {string -> atom}"""
w = CustomWorld()

if __name__ == "__main__":

    print()

    # try:
    #     x = w["r1"] & w["r2"]
    # except NotSatisfiableException:
    #     print("r1 and r2 are two mutually exclusive locations!")

    try:
        x = w["pi"] & w["gr"]
        print(x)
    except NotSatisfiableException:
        print("something went wrong")
