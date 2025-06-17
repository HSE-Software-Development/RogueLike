from abc import ABC, abstractmethod


class IManager(ABC):

    @abstractmethod
    def next_level(self, room_index: int):
        pass

    @abstractmethod
    def set_gameover(self):
        pass
