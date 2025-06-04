from abc import abstractmethod
from roguelike.game_objects.game_object import GameObject
from enum import Enum


class WeaponAttackPattern(Enum):
    NullType = 0
    MeleeType = 1
    RangeType = 2


class Weapon(GameObject):
    def __init__(self, position):
        super().__init__(position)

        self.attack_pattern = WeaponAttackPattern.NullType

        self.physical_damage = 0.0
        self.absolute_physical_armor_piercing = 0
        self.percentage_physical_armor_piercing = 0.0

        self.magical_damage = 0.0
        self.absolute_magical_armor_piercing = 0
        self.percentage_magical_armor_piercing = 0.0

    def on_attack(self, physical_armor: int, magical_armor: int) -> float:
        return self.physical_damage / min(
            (1 - self.percentage_physical_armor_piercing) * physical_armor
            - self.absolute_physical_armor_piercing,
            0.2,
        ) + self.magical_damage / min(
            (1 - self.percentage_magical_armor_piercing) * magical_armor
            - self.absolute_magical_armor_piercing,
            0.2,
        )
