#!/usr/bin/env python3

import sys
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"

import pygame
import jovialengine

import constants
import mode
from state import State


game = jovialengine.initGame(
    mode,
    mode.ModeOpening0,
    State,
    constants.SRC_DIRECTORY,
    constants.SCREEN_SIZE,
    constants.TITLE,
    constants.WINDOW_ICON,
    constants.FONT,
    constants.FONT_SIZE,
    constants.FONT_HEIGHT,
    constants.FONT_ANTIALIAS
)
game.start()
while game.run():
    pass

pygame.quit()
sys.exit()
