from roguelike.types import Cell
from roguelike.interfaces import *
from typing import Callable, override


class DamageAction(IRoomGameAction):
    def __init__(
        self,
        sender: IGameObject,
        hit: Callable[[list[IGameObjectWithPosition]], None],
        cells: list[Cell],
    ):
        self.hit = hit
        self.sender = sender
        self.cells = cells

    @override
    def room_handler(self, room: IRoom):
        from roguelike.game_objects.prey import Prey
        from roguelike.game_objects.prey.projectile import Projectile
        from roguelike.game_objects.weapons.melee_weapons.projectile_weapon import (
            ProjectileWeapon,
        )

        receivers: list[IGameObjectWithPosition] = []
        for cell in self.cells:
            for obj in room.objects:
                if obj == self.sender or not isinstance(obj, Prey):
                    continue
                if obj.cell == cell and not (
                    isinstance(self.sender, ProjectileWeapon)
                    and self.sender.owner == obj
                ):
                    receivers.append(obj)
        if len(receivers) > 0:
            # print(str(self.sender) + " " + str(receivers[0]))
            self.hit(receivers)
