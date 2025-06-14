from abc import ABC, abstractmethod
from .room import IRoom
from .game_action import IGameAction


class IRoomGameAction(IGameAction, ABC):

    @abstractmethod
    def room_handler(self, room: IRoom) -> None:
        pass
