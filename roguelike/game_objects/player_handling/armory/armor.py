from roguelike.game_objects.game_object import GameObject


class Armor(GameObject):
    def __init__(self, position):
        super().__init__(position)

        # absolute values or all kind of armors
        self.physical_armor = 0.0
        self.magical_armor = 0.0

        # who knows, knows
        self.vanguard_effect = 0.0


class OldRobe(Armor):
    def __init__(self, position):
        super().__init__(position)

        self.physical_armor = 10.0
        self.magical_armor = 5.0
