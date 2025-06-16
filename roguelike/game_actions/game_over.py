from roguelike.interfaces import *
from typing import override


class GameOverAction(IManagerGameAction):

    def __init__(self):
        pass

    @override
    def manager_handler(self, manager: IManager):
        manager.set_gameover()
