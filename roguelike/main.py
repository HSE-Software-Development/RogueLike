from .keyboard_manager import KeyboardManager
from .game_manager import GameManager


def main():
    keyboard = KeyboardManager()
    game_manager = GameManager(keyboard, margin_x=10, margin_y=2)

    keyboard.run()
    game_manager.run()


if __name__ == "__main__":
    main()
