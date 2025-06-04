from roguelike.game_objects.game_object import GameObject


class Spell(GameObject):
    def __init__(self, position):
        super().__init__(position)
