from roguelike.interfaces import *
from roguelike.types import Cell, Color, Effect
from typing import override


GAMEOVER = """\
  ____    _    __  __ _____ _____     _______ ____  
 / ___|  / \  |  \/  | ____/ _ \ \   / / ____|  _ \ 
| |  _  / _ \ | |\/| |  _|| | | \ \ / /|  _| | |_) |
| |_| |/ ___ \| |  | | |__| |_| |\ V / | |___|  _ < 
 \____/_/   \_\_|  |_|_____\___/  \_/  |_____|_| \_\
 """

GAMEWIN = """\
  ____    _    __  __ _______     __     ________   ___
 / ___|  / \  |  \/  | ____\ \   /  \   / /| ||  \  | |
| |  _  / _ \ | |\/| |  _|  \ \ / /\ \ / / | || \ \ | |
| |_| |/ ___ \| |  | | |__|  \ V /  \ V /  | || |\ \| |
 \____/_/   \_\_|  |_|_____|  \_/    \_/   |_||_| \___|
 """


class GameStatus(IGameObject):
    def __init__(self) -> None:
        super().__init__()
        self.is_win = False

    @override
    def on_init(self):
        pass

    @override
    def on_update(self, keyboard: IKeyboard):
        return []

    @override
    def on_draw(self, animation: IAnimation):
        if self.is_win:
            for y, line in enumerate(GAMEWIN.splitlines()):
                for x, char in enumerate(line):
                    if char != " ":
                        animation.draw(
                            Cell(x, y),
                            char,
                            color=Color.YELLOW,
                            z_buffer=5,
                            effects=[Effect.BOLD, Effect.BLINK],
                        )
        else:
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
