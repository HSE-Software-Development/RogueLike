from abc import ABC, abstractmethod


class IManager(ABC):

    @abstractmethod
    def next_level(self):
        pass
