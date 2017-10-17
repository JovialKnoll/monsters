#!/usr/bin/env python3.6

import sys

from game import Game

def main():
    game = Game()
    while game.run():
        pass
    del game
    sys.exit()

if __name__ == "__main__":
    main()
