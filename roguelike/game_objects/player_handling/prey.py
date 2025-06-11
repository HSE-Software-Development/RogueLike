from typing import List, override
from roguelike.game_actions.create_action import DeleteAction
from roguelike.game_actions.move_action import (
    MoveWithChildrenAction,
)
from roguelike.game_objects.player_handling.armory.armor import Armor
from roguelike.game_objects.player_handling.armory.melee_weapons import (
    MeleeWeapon,
    ProjectileWeapon,
)
from roguelike.types import Color, GameAction, GameObject
from roguelike.game_objects.player_handling.armory.weapon import Weapon
from roguelike.types import Cell
from roguelike.keyboard import is_pressed


class Prey(GameObject):
    def __init__(self, cell: Cell, health: int):
        super.__init__(cell)

        self.health = health
        self.armor = (
            Armor()
        )  # совсем не важно, как ты ударишь, а важно, какой держишь удар

    @override
    def on_update(self):
        if self.health <= 0:
            return [DeleteAction(self)]
        return []


class Projectile(Prey):
    def __init__(self, cell, health, direction):
        super().__init__(cell, health)

        self.projectile = ProjectileWeapon(cell, direction)

    @override
    def on_update(self) -> List[GameAction]:
        new_actions: GameAction = []
        new_actions.extend(super().on_update())
        if not self.is_deleted:
            new_actions.extend(self.projectile.on_update())
        return new_actions

    def on_draw(self, animation):
        animation.draw(self.cell, "~", color=Color.BLUE, z_buffer=5)


class NPC(Prey):
    def __init__(self, cell: Cell, health: int, armor: Armor, weapon: Weapon):
        super().__init__(cell, health)

        self.armor = armor
        self.weapon = weapon

        self.children.append(self.armor)
        self.children.append(self.weapon)

    def on_update(self):
        new_actions: List[GameAction] = []
        for object in self.children:
            new_actions.extend(object.on_update())
        new_actions.extend(super().on_update())
        return new_actions


class Player(NPC):
    def __init__(self, cell: Cell, health: int, armor: Armor, weapon: Weapon):
        super().__init__(cell, health)

        self.armor = armor
        self.weapon = weapon

        self.children.append(self.armor)
        self.children.append(self.weapon)

    @override
    def on_update(self):
        new_actions: List[GameAction] = []

        if is_pressed("w"):
            new_actions.append(
                MoveWithChildrenAction(self, Cell(self.cell.x, self.cell.y - 1))
            )
        elif is_pressed("s"):
            new_actions.append(
                MoveWithChildrenAction(self, Cell(self.cell.x, self.cell.y + 1))
            )
        elif is_pressed("a"):
            new_actions.append(
                MoveWithChildrenAction(self, Cell(self.cell.x - 1, self.cell.y))
            )
        elif is_pressed("d"):
            new_actions.append(
                MoveWithChildrenAction(self, Cell(self.cell.x + 1, self.cell.y))
            )

        new_actions.append(super().on_update())

        return new_actions

    def on_draw(self, animation):
        animation.draw(self.cell, "8", color=Color.RED, z_buffer=5)
