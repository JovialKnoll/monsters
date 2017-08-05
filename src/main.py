import sys

from game import *

def main():
    game = Game()
    while game.run():
        # stuff can be put here, in which case pass is not needed
        pass
    del game
    sys.exit()

if __name__ == "__main__":
    main()
