from abc import ABC, abstractmethod
from .level import ILevel
from .game_action import IGameAction


class ILevelGameAction(IGameAction, ABC):

    @abstractmethod
    def level_handler(self, level: ILevel) -> None:
        pass
