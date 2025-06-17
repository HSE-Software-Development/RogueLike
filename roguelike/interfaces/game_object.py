from abc import ABC, abstractmethod
from .animation import IAnimation
from .game_action import IGameAction
from .keyboard import IKeyboard


class IGameObject(ABC):
    @abstractmethod
    def on_init(self):
        pass

    @abstractmethod
    def on_draw(self, animation: IAnimation):
        pass

    @abstractmethod
    def on_update(self, keyboard: IKeyboard) -> list[IGameAction]:
        pass
