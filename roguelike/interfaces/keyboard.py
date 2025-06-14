from abc import ABC, abstractmethod


class IKeyboard(ABC):

    @abstractmethod
    def is_pressed(self, key: str) -> bool:
        """Check if a key is currently pressed."""
        pass

    @abstractmethod
    def pressed(self) -> list[str]:
        """Get a list of keys that are currently pressed."""
        pass
