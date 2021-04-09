from goal import Goal


def __str__(self, level=0):
    """Print current Goal"""
    ret = Goal.pretty_print_goal(self, level)

    if self.children is not None:

        for link, goals in self.children.items():

            ret += "\t" * level + "|  " + link.name + "\n"
            level += 1
            for child in goals:
                try:
                    ret += child.__str__(level + 1)
                except:
                    print("ERROR IN PRINT")
    return ret
