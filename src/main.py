#!/usr/bin/env python3

import sys
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
import pygame
pygame.init()

from game import Game
from mode import ModeOpening0


def main():
    game = Game(ModeOpening0())
    while game.run():
        pass
    del game


if __name__ == "__main__":
    main()
pygame.quit()
sys.exit()
