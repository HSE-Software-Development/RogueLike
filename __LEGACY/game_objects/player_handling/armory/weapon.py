from __future__ import annotations
from abc import abstractmethod
from typing import List
from roguelike.types import GameAction, GameObject
from roguelike.game_objects.player_handling.armory.armor import IArmor
from roguelike.keyboard import is_pressed
from enum import Enum
import time


class WeaponAttackPattern(Enum):
    NullType = 0
    MeleeType = 1
    RangeType = 2


class IWeapon(GameObject):
    def __init__(self, cell):
        super().__init__(cell)

        self.attack_pattern = WeaponAttackPattern.NullType
        self.attack_speed = 0.0  # times per second
        self.previous_time = -1.0

        self.physical_damage = 0.0
        self.absolute_physical_armor_piercing = 0
        self.percentage_physical_armor_piercing = 0.0

        self.magical_damage = 0.0
        self.absolute_magical_armor_piercing = 0
        self.percentage_magical_armor_piercing = 0.0

    def set_all_damage_params(
        self,
        physical_damage,
        percentage_physical_armor_piercing,
        absolute_physical_armor_piercing,
        magical_damage=0,
        percentage_magical_armor_piercing=0,
        absolute_magical_armor_piercing=0,
    ):
        self.physical_damage = physical_damage
        self.percentage_physical_armor_piercing = percentage_physical_armor_piercing
        self.absolute_physical_armor_piercing = absolute_physical_armor_piercing

        self.magical_damage = magical_damage
        self.percentage_magical_armor_piercing = percentage_magical_armor_piercing
        self.absolute_magical_armor_piercing = absolute_magical_armor_piercing

    def set_same(self, weapon: IWeapon):
        self.physical_damage = weapon.physical_damage
        self.percentage_physical_armor_piercing = (
            weapon.percentage_physical_armor_piercing
        )
        self.absolute_physical_armor_piercing = weapon.absolute_physical_armor_piercing

        self.magical_damage = weapon.magical_damage
        self.percentage_magical_armor_piercing = (
            weapon.percentage_magical_armor_piercing
        )
        self.absolute_magical_armor_piercing = weapon.absolute_magical_armor_piercing

    def set_physical_damage_params(
        self,
        physical_damage,
        percentage_physical_armor_piercing,
        absolute_physical_armor_piercing,
    ):
        self.physical_damage = physical_damage
        self.percentage_physical_armor_piercing = percentage_physical_armor_piercing
        self.absolute_physical_armor_piercing = absolute_physical_armor_piercing

    def set_magical_damage_params(
        self,
        magical_damage,
        percentage_magical_armor_piercing,
        absolute_magical_armor_piercing,
    ):
        self.magical_damage = magical_damage
        self.percentage_magical_armor_piercing = percentage_magical_armor_piercing
        self.absolute_magical_armor_piercing = absolute_magical_armor_piercing

    def __is_attack_time(self) -> bool:
        current_time = time.monotonic()

        if self.previous_time == -1.0:
            self.previous_time = current_time
        elapsed_time = current_time - self.previous_time

        if self.attack_speed == 0.0 or elapsed_time >= 1.0 / self.attack_speed:
            self.previous_time = current_time
            return True
        return False

    def __calculate_damage(self, armor: IArmor) -> float:
        """
        Damage concept: on actions interaction between a player/mob and a weapon provided by weapon functional.
            All data about resists, etc. will be received from armor class
        """

        return abs(self.physical_damage - armor.vanguard_effect) / max(
            (1 - self.percentage_physical_armor_piercing) * armor.physical_armor
            - self.absolute_physical_armor_piercing,
            1.0,
        ) + self.magical_damage / max(
            (1 - self.percentage_magical_armor_piercing) * armor.magical_armor
            - self.absolute_magical_armor_piercing,
            1.0,
        )

    def hit(weapon: IWeapon, objects: List["Prey"]) -> List[GameAction]:
        if weapon.__is_attack_time():
            for Prey in objects:
                damage = weapon.__calculate_damage(Prey.armor)
                Prey.health -= damage
        return []

    def on_update(self):
        return []

    def on_draw(self, animation):
        pass
