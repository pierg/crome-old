from core.cgg import Node
from examples.goals.create_goals import set_of_goals
from examples.types.create_world import ExampleWorld

w = ExampleWorld()


def build_cgg():

    """Automatically build the CGG."""
    cgg = Node.build_cgg(set_of_goals)
    print(cgg)


if __name__ == "__main__":
    build_cgg()
