from roguelike.types import Animation
from roguelike.keyboard import _listener
import curses


def main(stdscr):
    animation = Animation(stdscr, width=140, height=35)
    # animation = Animation(width=50, height=20)

    _listener.start()
    animation._start()

    animation._stop()
    _listener.join()

    # print("hello")
    # listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    # listener.start()
    # listener.join()


if __name__ == "__main__":
    curses.wrapper(main)
    # main()
