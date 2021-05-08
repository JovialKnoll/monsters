#!/usr/bin/env python3

import sys

import pygame

from game import Game


def main():
    pygame.init()
    game = Game()
    while game.run():
        pass
    del game
    pygame.quit()


if __name__ == "__main__":
    main()

sys.exit()
