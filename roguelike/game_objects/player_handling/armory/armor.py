from roguelike.types import Color, GameObject


class Armor(GameObject):
    def __init__(self, position):
        super().__init__(position)

        # absolute values or all kind of armors
        self.physical_armor = 0.0
        self.magical_armor = 0.0

        # who knows, knows
        self.vanguard_effect = 0.0

    def init():
        pass

    def on_update(self, room):
        return []

    def on_draw(self, animation):
        pass


class OldRobe(Armor):
    def __init__(self, position):
        super().__init__(position)

        self.physical_armor = 10.0
        self.magical_armor = 5.0

    def init(self):
        pass

    def on_draw(self, animation):
        animation.draw(self.cell, "@", color=Color.BLUE, z_buffer=5)

    def on_update(self):
        return []
