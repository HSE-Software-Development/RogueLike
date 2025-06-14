from .keyboard_manager import KeyboardManager
from .game_manager import GameManager
import sys
import tty
import termios
import curses


def main(stdscr):
    # fd = sys.stdin.fileno()
    # old_settings = termios.tcgetattr(fd)
    # tty.setcbreak(fd)

    curses.curs_set(0)  # Скрыть курсор
    stdscr.nodelay(1)  # Неблокирующий ввод

    keyboard = KeyboardManager()
    game_manager = GameManager(
        stdscr,
        keyboard,
        margin_x=4,
        margin_y=2,
        width=140,
        height=38,
    )

    keyboard.run()
    game_manager.run()


if __name__ == "__main__":
    curses.wrapper(main)
