from core.world import World


class CustomWorld(World):
    def __init__(self):
        super().__init__(
            actions={Picture()},
            locations={
                R1(),
                R2(),
                R5(),
                R4(),
            },
            sensors={Movement()},
        )
