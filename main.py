import argparse
from curses import wrapper
from classes import Game

INTRO = """Welcome to Solitaire!
This is a port of Solitaire, more specifically Klondike, to the terminal.

The following options are available:
    1) Start a new game, using turn 1.
    2) Start a new game, using turn 3.
    3) Quit the game.
"""

# ? Main game loop. Handles all actions involving curses. Ideally, this should be the only thing that uses curses. Do not pass stdscr to any other functions.
def main(stdscr):
    stdscr.clear()
    stdscr.addstr(INTRO)
    while True:
        mainChoice = stdscr.getch()
        if mainChoice == ord('1') or mainChoice == ord('2'): # The actual game loop begins here.
            game = Game(mainChoice == ord('2'))
            while True:
                stdscr.clear()
                stdscr.addstr(game.drawGame())
                c = stdscr.getch()
                if c == ord('d'):
                    game.drawNewWaste()
                elif c == ord('q'):
                    return
        elif mainChoice == ord('3'):
            break

# Init.
if __name__ == "__main__":
    wrapper(main)
