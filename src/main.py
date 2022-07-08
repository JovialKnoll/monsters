#!/usr/bin/env python3

import sys
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"

import pygame
import jovialengine

game = jovialengine.getGame()

from mode import ModeOpening0

game.load(ModeOpening0)
while game.run():
    pass

pygame.quit()
sys.exit()
