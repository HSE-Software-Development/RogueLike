from abc import ABC, abstractmethod
from .level import ILevel
from .game_action import IGameAction
from .manager import IManager


class IManagerGameAction(IGameAction, ABC):

    @abstractmethod
    def manager_handler(self, manager: IManager) -> None:
        pass
