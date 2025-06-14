from abc import ABC, abstractmethod


class ILevel(ABC):

    @abstractmethod
    def move_player(self, prev_room: int, next_room: int, door_index: int):
        pass
