from roguelike.interfaces import IKeyboard
from typing import override
from pynput import keyboard as pynput_keyboard


class KeyboardManager(IKeyboard):

    def __init__(self):
        self._listener = pynput_keyboard.Listener(
            on_press=self._on_pressed,
            on_release=self._on_release,
            daemon=True,
        )
        self._key_pressed: dict[str, bool] = {}

    def _on_pressed(self, key):
        try:
            key_char = key.char
        except AttributeError:
            key_char = key.name

        self._key_pressed[key_char] = True

    def _on_release(self, key):
        try:
            key_char = key.char
        except AttributeError:
            key_char = key.name

        self._key_pressed[key_char] = False

    @override
    def is_pressed(self, key: str) -> bool:
        return self._key_pressed.get(key, False)

    @override
    def pressed(self) -> list[str]:
        return [key for key, pressed in self._key_pressed.items() if pressed]

    def run(self):
        self._listener.start()

    def stop(self):
        # self._listener.stop()
        pass
