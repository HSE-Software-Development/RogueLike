from roguelike.game_objects.armor.old_robe import OldRobe
from roguelike.game_objects.weapons.range_weapons.wood_bow import WoodBow
from roguelike.interfaces import *
from roguelike.game_objects import Level
from roguelike.animation import Animation
from roguelike.types import Rect, Cell, Color
import time
from roguelike.game_objects.prey import Player
from roguelike.game_objects.armor import Armor
from roguelike.game_objects.weapons import Weapon
from roguelike.game_objects import HUD
from roguelike.game_objects import GameOver
from roguelike.game_objects.game_over import GAMEOVER
from roguelike.game_objects.prey.inventory import Inventory
import curses
from typing import override


class GameManager(IManager):

    def __init__(
        self,
        stdscr,
        keyboard: IKeyboard,
        margin_x: int = 0,
        margin_y: int = 0,
        width: int = 140,
        height: int = 38,
    ):
        self._stdscr = stdscr
        self._width = width
        self._height = height
        self._keyboard = keyboard
        self._animation = Animation(
            stdscr, margin_x=margin_x, margin_y=margin_y, width=width, height=height
        )
        self.level_width = width
        self.level_height = height - 10
        self.game_status: int = -1  # 0 for over, 1 for win

        self._player = Player(
            health=10,
            cell=Cell(1, 1),
            armor=OldRobe(Cell(1, 1)),
            weapon=WoodBow(Cell(1, 1)),
        )
        self._cur_level_index = 0
        self._levels: list[Level] = []
        self._game_over = GameOver()
        self._hud = HUD(self._player, int(self._player.max_health))

    def _init(self):
        number_of_levels = 3
        for i in range(number_of_levels):
            self._levels.append(
                Level(
                    rect=Rect(
                        lt=Cell(0, 0),
                        rb=Cell(self.level_width - 1, self.level_height - 1),
                    ),
                    difficulty=(i + 1) / number_of_levels,
                )
            )
        for level in self._levels:
            level.on_init()

        self._levels[self._cur_level_index].set_player(self._player)

    def _update(self):
        if self.game_status < 0:
            actions = []
            actions.extend(self._hud.on_update(self._keyboard))
            actions.extend(
                self._levels[self._cur_level_index].on_update(self._keyboard)
            )

            for action in actions:
                if isinstance(action, IManagerGameAction):
                    action.manager_handler(self)

    def _draw(self):
        if self.game_status < 0:
            self._hud.on_draw(
                self._animation.with_area(
                    margin_x=0,
                    margin_y=self.level_height + 1,
                    width=self._width,
                    height=6,
                )
            )

            self._levels[self._cur_level_index].on_draw(
                self._animation.with_area(
                    margin_x=0,
                    margin_y=0,
                    width=self.level_width,
                    height=self.level_height,
                )
            )

            self._animation.print(
                f"Level: {self._cur_level_index + 1}/{len(self._levels)}",
                color=Color.RED,
            )
        else:
            if self.game_status == 1:
                self._game_over.is_win = True
            self._game_over.on_draw(
                self._animation.with_area(
                    margin_x=self._width // 2 - len(GAMEOVER.splitlines()[0]) // 2,
                    margin_y=self._height // 2 - len(GAMEOVER.splitlines()) // 2,
                    width=self._width,
                    height=self._height,
                )
            )

    def _game_loop(self):
        self._init()
        while True:
            if self._keyboard.is_pressed("p"):
                return

            self._update()

            self._draw()
            self._animation.render()

            self._animation.clear()

    def run(self):
        self._game_loop()

    @override
    def next_level(self, room_index: int):
        if not self._levels[self._cur_level_index].key_picked:
            return
        if self._cur_level_index == len(self._levels) - 1:
            self.game_status = 1
            return

        from roguelike.game_objects.prey.inventory import ItemType

        self._player.inventory.remove_key()
        self._levels[self._cur_level_index].remove_player(room_index=room_index)
        self._cur_level_index = min(self._cur_level_index + 1, len(self._levels) - 1)
        self._levels[self._cur_level_index].set_player(self._player)

    def set_gameover(self):
        self.game_status = 0
