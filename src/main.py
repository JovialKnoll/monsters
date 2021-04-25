#!/usr/bin/env python3

import sys

import pygame

from game import Game


def main():
    pygame.init()
    # grab the below from an ini file in the future
    max_framerate = 170
    game = Game(max_framerate)
    while game.run():
        pass
    del game
    pygame.quit()


if __name__ == "__main__":
    main()

sys.exit()
