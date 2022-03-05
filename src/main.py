#!/usr/bin/env python3

import sys
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
import pygame
pygame.init()

import jovialengine

from mode import ModeOpening0


def main():
    game = jovialengine.Game(ModeOpening0())
    while game.run():
        pass
    del game


if __name__ == "__main__":
    main()
pygame.quit()
sys.exit()
