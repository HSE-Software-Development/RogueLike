from abc import ABCMeta
from roguelike.game_actions.collect_item import CollectItemAction
from roguelike.game_actions.create import CreateAction
from roguelike.game_actions.game_over import GameOverAction
from roguelike.game_actions.remove import RemoveAction
from roguelike.game_actions.sleep import SleepAction
from roguelike.game_objects.game_over import GameOver
from roguelike.game_objects.armor import Armor
from roguelike.game_objects.prey.prey import Prey
from roguelike.interfaces.game_action import IGameAction
from roguelike.interfaces.game_object_with_position import IGameObjectWithPosition
from roguelike.interfaces.item_types import ItemType
from roguelike.interfaces.keyboard import IKeyboard
from roguelike.types import Cell, Color, Effect
from roguelike.game_objects.weapons import Weapon
from roguelike.game_objects.weapons.range_weapons.range_weapon import RangeWeapon
from roguelike.game_actions import MoveAction
from typing import Optional, override
from .inventory import Inventory, InventoryItem


class Player(Prey):
    def __init__(self, cell: Cell, health: float, armor: Armor, weapon: Weapon):
        super().__init__(cell, health, armor, weapon)

        self.update_time = 10.0  # per 1 second
        self.direction = Cell(1, 0)

    def register_item(self, item: IGameObjectWithPosition):
        item.cell = self.cell
        if isinstance(item, Weapon):
            for iitem in self.inventory.items:
                if (
                    iitem != None
                    and isinstance(iitem.obj, Weapon)
                    and item != iitem.obj
                ):
                    iitem.type = ItemType.WEAPON
            self.weapon = item
            item.in_hands = True
        if isinstance(item, Armor):
            for iitem in self.inventory.items:
                if iitem != None and isinstance(iitem.obj, Armor) and item != iitem.obj:
                    iitem.type = ItemType.ARMOR
            self.armor = item
        self.children.append(item)

    def activate_item(self, item: Optional[InventoryItem]):
        if item == None:
            return
        if isinstance(item.obj, Weapon):
            for iitem in self.inventory.items:
                if (
                    iitem != None
                    and isinstance(iitem.obj, Weapon)
                    and item != iitem.obj
                ):
                    iitem.type = ItemType.WEAPON
            if item.type == ItemType.BOW:
                item.type = ItemType.ACTIVE_BOW
                self.register_item(item.obj)
            elif item.type == ItemType.SWORD:
                item.type = ItemType.ACTIVE_SWORD
                self.register_item(item.obj)
            elif item.type == ItemType.WEAPON:
                item.type = ItemType.ACTIVE_WEAPON
                self.register_item(item.obj)
        if isinstance(item.obj, Armor):
            if item.type == ItemType.ARMOR:
                item.type = ItemType.ACTIVE_ARMOR
                self.register_item(item.obj)

    @override
    def on_update(self, keyboard: IKeyboard) -> list[IGameAction]:
        new_actions: list[IGameAction] = []

        # Чтобы не активированные шмотки с нами ходили (их нет в детях и их по другому двигать не получается)
        for item in self.inventory.items:
            if item is not None:
                item.obj.cell = self.cell

        if self.health <= 0:
            return [RemoveAction(self), SleepAction(1.5), GameOverAction()]
        if keyboard.is_pressed("o"):
            if self.weapon != None:
                new_actions.extend(self.weapon.on_update(keyboard))
        if not self.is_update_time():
            return new_actions

        if keyboard.is_pressed("w"):
            self.direction = Cell(0, -1)
            new_actions.append(MoveAction(object=self, cell=self.cell + self.direction))
        elif keyboard.is_pressed("s"):
            self.direction = Cell(0, 1)
            new_actions.append(MoveAction(object=self, cell=self.cell + self.direction))
        elif keyboard.is_pressed("a"):
            self.direction = Cell(-1, 0)
            new_actions.append(MoveAction(object=self, cell=self.cell + self.direction))
        elif keyboard.is_pressed("d"):
            self.direction = Cell(1, 0)
            new_actions.append(MoveAction(object=self, cell=self.cell + self.direction))
        if keyboard.is_pressed("g"):
            drop = self.inventory.get_item()
            if drop is not None:
                if drop.obj == self.weapon:
                    self.weapon.in_hands = False
                    self.weapon = None
                if drop.obj == self.armor:
                    self.armor = None
                try:
                    self.children.remove(drop.obj)
                except ValueError as e:
                    drop.type = ItemType.NONE
                new_actions.extend(self.inventory.drop_item())
        if keyboard.is_pressed("e"):
            if self.inventory.get_item() == None:
                new_actions.append(
                    CollectItemAction([self.cell], self.inventory.add_item)
                )
        if keyboard.is_pressed("q"):
            self.activate_item(self.inventory.get_item())

        if isinstance(self.weapon, RangeWeapon):
            if len(self.weapon.directions) == 1:
                self.weapon.directions = [self.direction]

        return new_actions

    def on_draw(self, animation):
        for child in self.children:
            child.on_draw(animation)
        animation.draw(self.cell, "*", color=Color.BLACK_RED, z_buffer=5)
