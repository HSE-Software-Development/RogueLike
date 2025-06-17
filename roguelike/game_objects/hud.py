from roguelike.interfaces import *
from roguelike.types import Cell, Rect, Color, Effect
from typing import override, Optional
from .prey import Player
from enum import Enum
from roguelike.game_objects.prey.inventory import InventoryItem, ItemType

NONE = """\
**    **
** *  **
**  * **
**    **
"""

ARMOR = """\
##****##
##****##
| **** |
  ****
"""

WEAPON = """\
   *****
     ***
  **   *
**
"""

HEART = """\
 **  **
********
 ******
   **
"""

SWORD = """\
   *
   *
  ~~~
   #
"""

BOW = """\
  |%
  | $
  | $
  |%
"""

POTION = """\
   _
   | 
  / \\
  \\ /
"""

KEY = """\
   $>
   $>
   $
  [=]
"""

CELL_WIDTH = 9
CELL_HEIGHT = 6


class HUD(IGameObject):
    def __init__(self, player: Player, max_health: int):
        self.player = player
        self.max_health = max_health

    def set_target(self, index: int):
        self.player.inventory.select_item(index)

    def draw_heart(
        self,
        animation: IAnimation,
        cell: Cell,
        dead: bool = False,
    ):
        for y, line in enumerate(HEART.splitlines()):
            for x, char in enumerate(line):
                if char == "*":
                    if dead:
                        animation.draw(
                            Cell(cell.x + x, cell.y + y),
                            "#",
                            color=Color.RED,
                            z_buffer=5,
                            effects=[Effect.BLINK],
                        )
                    else:
                        animation.draw(
                            Cell(cell.x + x, cell.y + y),
                            " ",
                            color=Color.BLACK_RED,
                            z_buffer=5,
                            effects=[],
                        )

    def draw_sword(
        self,
        animation: IAnimation,
        cell: Cell,
    ):
        for y, line in enumerate(SWORD.splitlines()):
            for x, char in enumerate(line):
                if char != " ":
                    if char == "*":
                        animation.draw(
                            Cell(cell.x + x, cell.y + y),
                            " ",
                            color=Color.BLACK_YELLOW,
                            z_buffer=5,
                        )
                    else:
                        animation.draw(
                            Cell(cell.x + x, cell.y + y),
                            char,
                            color=Color.YELLOW,
                            z_buffer=5,
                            effects=[Effect.BOLD],
                        )

    def draw_bow(
        self,
        animation: IAnimation,
        cell: Cell,
    ):
        for y, line in enumerate(BOW.splitlines()):
            for x, char in enumerate(line):
                if char != " ":
                    animation.draw(
                        Cell(cell.x + x, cell.y + y),
                        char,
                        color=Color.YELLOW,
                        z_buffer=5,
                        effects=[Effect.BOLD],
                    )

    def draw_potion(
        self,
        animation: IAnimation,
        cell: Cell,
    ):
        for y, line in enumerate(POTION.splitlines()):
            for x, char in enumerate(line):
                if char != " ":
                    animation.draw(
                        Cell(cell.x + x, cell.y + y),
                        char,
                        color=Color.YELLOW,
                        z_buffer=5,
                        effects=[Effect.BOLD],
                    )

    def draw_key(
        self,
        animation: IAnimation,
        cell: Cell,
    ):
        for y, line in enumerate(KEY.splitlines()):
            for x, char in enumerate(line):
                if char != " ":
                    animation.draw(
                        Cell(cell.x + x, cell.y + y),
                        char,
                        color=Color.YELLOW,
                        z_buffer=5,
                        effects=[Effect.BOLD],
                    )

    def draw_weapon(
        self,
        animation: IAnimation,
        cell: Cell,
    ):
        for y, line in enumerate(WEAPON.splitlines()):
            for x, char in enumerate(line):
                if char != " ":
                    animation.draw(
                        Cell(cell.x + x, cell.y + y),
                        char,
                        color=Color.CYAN,
                        z_buffer=5,
                        effects=[Effect.BOLD],
                    )

    def draw_none(
        self,
        animation: IAnimation,
        cell: Cell,
    ):
        for y, line in enumerate(NONE.splitlines()):
            for x, char in enumerate(line):
                if char != " ":
                    animation.draw(
                        Cell(cell.x + x, cell.y + y),
                        char,
                        color=Color.RED,
                        z_buffer=5,
                        effects=[Effect.BOLD],
                    )

    def draw_armor(
        self,
        animation: IAnimation,
        cell: Cell,
    ):
        for y, line in enumerate(ARMOR.splitlines()):
            for x, char in enumerate(line):
                if char != " ":
                    animation.draw(
                        Cell(cell.x + x, cell.y + y),
                        char,
                        color=Color.WHITE,
                        z_buffer=5,
                        effects=[Effect.BOLD],
                    )

    def draw_inventory_cell(
        self,
        animation: IAnimation,
        cell: Cell,
        item: Optional[InventoryItem],
        is_target: bool = False,
    ):
        def draw_rect(rect: Rect, fill: bool = False):
            for y in range(rect.lt.y, rect.rb.y + 1):
                for x in range(rect.lt.x, rect.rb.x + 1):
                    if fill or (
                        x == rect.lt.x
                        or x == rect.rb.x
                        or y == rect.lt.y
                        or y == rect.rb.y
                    ):
                        if is_target:
                            animation.draw(
                                Cell(x, y),
                                " ",
                                color=Color.BLACK_GREEN,
                                z_buffer=6,
                            )
                        else:
                            animation.draw(
                                Cell(x, y),
                                " ",
                                color=Color.BLACK_WHITE,
                                z_buffer=5,
                            )

        draw_rect(
            Rect(
                Cell(cell.x, cell.y),
                Cell(cell.x + CELL_WIDTH - 1, cell.y + CELL_HEIGHT - 1),
            )
        )
        cell = Cell(cell.x + 1, cell.y + 1)
        if item is None:
            return
        if item.type == ItemType.SWORD:
            self.draw_sword(animation, cell)
        elif item.type == ItemType.BOW:
            self.draw_bow(animation, cell)
        elif item.type == ItemType.POTION:
            self.draw_potion(animation, cell)
        elif item.type == ItemType.KEY:
            self.draw_key(animation, cell)
        elif item.type == ItemType.WEAPON:
            self.draw_weapon(animation, cell)
        elif item.type == ItemType.ARMOR:
            self.draw_armor(animation, cell)
        else:
            self.draw_none(animation, cell)

    def draw_inventory(
        self,
        animation: IAnimation,
        cell: Cell,
    ):
        for i, item in enumerate(self.player.inventory.items):
            self.draw_inventory_cell(
                animation=animation,
                cell=Cell(cell.x + i * (CELL_WIDTH - 1), cell.y + 0),
                item=item,
                is_target=(i == self.player.inventory.current),
            )

    @override
    def on_draw(self, animation: IAnimation):
        for i in range(self.max_health):
            if i < self.player.health:
                self.draw_heart(
                    animation=animation,
                    cell=Cell(i * 10, 0),
                    dead=False,
                )
            else:
                self.draw_heart(
                    animation=animation,
                    cell=Cell(i * 10, 0),
                    dead=True,
                )
        self.draw_inventory(animation, Cell(self.max_health * 10 + 20, 0))

    @override
    def on_init(self):
        pass

    @override
    def on_update(self, keyboard: IKeyboard) -> list[IGameAction]:
        for i in range(len(self.player.inventory.items)):
            if keyboard.is_pressed(str(i + 1)):
                self.set_target(i)
                return []
        return []
