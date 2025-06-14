from pynput import keyboard


def is_pressed(key: str) -> bool:
    if key in _key_pressed:
        return _key_pressed[key]
    return False


def pressed() -> list[str]:
    res = []
    for key, pressed in _key_pressed.items():
        if pressed:
            res.append(key)
    return res


_key_pressed: dict[str, bool] = {}


def _on_press(key):
    try:
        key_char = key.char
    except AttributeError:
        key_char = key.name

    _key_pressed[key_char] = True


def _on_release(key):
    try:
        key_char = key.char
    except AttributeError:
        key_char = key.name
    _key_pressed[key_char] = False


_listener = keyboard.Listener(on_press=_on_press, on_release=_on_release)
