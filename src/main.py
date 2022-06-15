#!/usr/bin/env python3

import sys
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
import pygame
pygame.init()
import jovialengine
game = jovialengine.game.getInstance()
from mode import ModeOpening0
game.load(ModeOpening0)

while game.run():
    pass

del game
pygame.quit()
sys.exit()
