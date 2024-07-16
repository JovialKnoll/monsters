#!/usr/bin/env python3

import sys

import jovialengine

import constants
import mode
from state import State


game = jovialengine.init(
    mode,
    mode.ModeOpening0,
    State,
    constants.SRC_DIRECTORY,
    constants.SCREEN_SIZE,
    constants.TITLE,
    constants.WINDOW_ICON,
    1,
    constants.EVENT_NAMES,
    constants.INPUT_DEFAULTS,
    constants.FONT,
    constants.FONT_SIZE,
    constants.FONT_HEIGHT,
    constants.FONT_ANTIALIAS
)
while game.run():
    pass

sys.exit()
