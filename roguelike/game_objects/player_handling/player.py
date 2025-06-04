from typing import List
from roguelike.game_objects import GameObject
from roguelike.game_objects.player_handling.weapons.weapon import Weapon
from roguelike.types import Cell


class Player(GameObject):
    def __init__(self, position: Cell):
        super.__init__(position)

        weapons: List[Weapon] = []
