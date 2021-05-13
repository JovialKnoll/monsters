#!/usr/bin/env python3

import faulthandler
faulthandler.enable()

import sys

import pygame

from game import Game


def main():
    game = Game()
    while game.run():
        pass
    del game


pygame.init()
if __name__ == "__main__":
    main()
pygame.quit()
sys.exit()
