#!/usr/bin/env python3.6

import sys

from game import Game

def main():
    # grab the below from an ini file in the future
    max_framerate = 60
    game = Game(max_framerate)
    while game.run():
        pass
    del game
    sys.exit()

if __name__ == "__main__":
    main()
