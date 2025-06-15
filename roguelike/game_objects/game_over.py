from roguelike.interfaces import *
from roguelike.types import Cell, Color, Effect
from typing import override


GAMEOVER = """\
  ____    _    __  __ _____ _____     _______ ____  
 / ___|  / \  |  \/  | ____/ _ \ \   / / ____|  _ \ 
| |  _  / _ \ | |\/| |  _|| | | \ \ / /|  _| | |_) |
| |_| |/ ___ \| |  | | |__| |_| |\ V / | |___|  _ < 
 \____/_/   \_\_|  |_|_____\___/  \_/  |_____|_| \_\\"""


class GameOver(IGameObject):

    @override
    def on_init(self):
        pass

    @override
    def on_update(self, keyboard: IKeyboard):
        return []

    @override
    def on_draw(self, animation: IAnimation):
        for y, line in enumerate(GAMEOVER.splitlines()):
            for x, char in enumerate(line):
                if char != " ":
                    animation.draw(
                        Cell(x, y),
                        char,
                        color=Color.RED,
                        z_buffer=5,
                        effects=[Effect.BOLD, Effect.BLINK],
                    )
