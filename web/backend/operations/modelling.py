from tools.persistence import Persistence
from world import World


class Modelling:

    @staticmethod
    def create_environment(project_folder):

        # TODO: Substitute below with the parameters loaded from the JSON in 'project_folder'
        w = World(project_name="fill_project_id")
        w.new_boolean_action("greet")
        w.new_boolean_action("register")
        w.new_boolean_sensor("person")
        w.new_boolean_location("r1", mutex="locations", adjacency={"r2", "r5"})
        w.new_boolean_location("r2", mutex="locations", adjacency={"r1", "r5"})
        w.new_boolean_location("r5", mutex="locations", adjacency={"r1", "r2", "r3", "r4"})
        w.new_boolean_location("r3", mutex="locations", adjacency={"r4", "r5"})
        w.new_boolean_location("r4", mutex="locations", adjacency={"r3", "r5"})
        w.new_boolean_context("day", mutex="time")
        w.new_boolean_context("night", mutex="time")

        # TODO: save the world instance in the project_folder
        Persistence.dump_world(w, project_folder)