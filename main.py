import curses
from classes import Game

INTRO = """Welcome to Solitaire!
This is a port of Solitaire, more specifically Klondike, to the terminal.

The following options are available:
    1) Start a new game, using turn 1.
    2) Start a new game, using turn 3.
    3) Quit the game.

To avoid inconsistency with the module curses, please play the game with the terminal in fullscreen mode.
Requires 256-color (xterm-256) support. Support is indicated if the heart is visible and is pink: """

# ? Main game loop. Handles all actions involving curses. Ideally, this should be the only thing that uses curses. Do not pass stdscr to any other functions.
def main(stdscr):
    stdscr.clear()
    stdscr.addstr(INTRO)
    stdscr.addstr("♥\n", curses.color_pair(202))
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS - 1):
        curses.init_pair(i + 1, i, -1)

    while True:
        mainChoice = stdscr.getch()
        if mainChoice == ord('1') or mainChoice == ord('2'): # The actual game loop begins here.
            game = Game(mainChoice == ord('2'))
            while True:
                stdscr.clear()
                gameString = game.drawGame()
                for char in gameString:
                    if char == "♥":
                        stdscr.addstr("♥", curses.color_pair(197))
                    elif char == "♦":
                        stdscr.addstr("♦", curses.color_pair(197))
                    elif char == "/":
                        stdscr.addstr("/", curses.color_pair(240))
                    else:
                        stdscr.addstr(char)
                c = stdscr.getch()
                if c == ord('d'):
                    game.drawNewWaste()
                elif c == ord('r'):
                    game.resetWaste()
                elif c == ord('q'):
                    return
                elif c == 27: # Escape
                    game.putBackCard()
                elif c == 259: # Up Arrow
                    game.cursorMoveUp()
                elif c == 258: # Down Arrow
                    game.cursorMoveDown()
                elif c == 260: # Left Arrow
                    game.cursorMoveLeft()
                elif c == 261: # Right Arrow
                    game.cursorMoveRight()
                elif c == ord('1'):
                    game.cursorpos = 9 # Foundation 1
                elif c == ord('2'):
                    game.cursorpos = 10 # Foundation 2
                elif c == ord('3'):
                    game.cursorpos = 11 # Foundation 3
                elif c == ord('4'):
                    game.cursorpos = 12 # Foundation 4
                elif c == ord('5'):
                    game.cursorpos = 8 # Waste
                elif c == ord('c'):
                    game.grabSelectedCard()
                elif c == ord('v'):
                    game.placeGrabbedCard()
                elif c == ord('f'):
                    game.autoMoveToFoundation()
                elif c == ord('t'):
                    game.printTimeOnNextDraw()
                elif c == ord('n'):
                    game.newGame()
                elif c == ord ('y'):
                    if game.newGameState:
                        game = Game(mainChoice == ord('2'))
        elif mainChoice == ord('3') or mainChoice == ord('q'):
            break

# Init.
if __name__ == "__main__":
    curses.wrapper(main)
