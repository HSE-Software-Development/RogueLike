from roguelike.game_objects.player_handling.weapons.weapon import Weapon


class RangeWeapon(Weapon):
    def __init__(self, position):
        super().__init__(position)
