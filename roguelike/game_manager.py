from roguelike.interfaces import IKeyboard
from roguelike.game_objects import Level
from roguelike.animation import Animation
from roguelike.types import Rect, Cell
import time
from roguelike.game_objects.prey import Player
from roguelike.game_objects.armor import Armor
from roguelike.game_objects.weapons import Weapon
from roguelike.game_objects import HUD
import curses


class GameManager:

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

        self._levels: list[Level] = []
        self._player = Player(
            armor=Armor(Cell(0, 0)),
            weapon=Weapon(Cell(0, 0)),
            health=100,
            cell=Cell(1, 1),
        )
        self._hud = HUD()

    def _init(self):
        self._levels.append(
            Level(
                rect=Rect(
                    lt=Cell(0, 0), rb=Cell(self.level_width - 1, self.level_height - 1)
                )
            )
        )
        for level in self._levels:
            level.on_init()
            level.set_player(self._player)

    def _update(self):
        self._hud.on_update(self._keyboard)
        for level in self._levels:
            level.on_update(self._keyboard)

    def _draw(self):
        self._hud.on_draw(
            self._animation.with_area(
                margin_x=0,
                margin_y=self.level_height + 1,
                width=self._width,
                height=6,
            )
        )

        for level in self._levels:
            level.on_draw(
                self._animation.with_area(
                    margin_x=0,
                    margin_y=0,
                    width=self.level_width,
                    height=self.level_height,
                )
            )

    def _game_loop(self):
        self._init()
        while True:
            self._update()

            self._draw()
            self._animation.render()

            curses.napms(50)
            self._animation.clear()

    def run(self):
        self._game_loop()
