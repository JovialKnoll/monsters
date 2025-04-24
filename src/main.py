#!/usr/bin/env python3

import sys

import jovialengine

import constants
import mode
from state import State

game = jovialengine.GameBuilder()\
    .set_mode_module(mode)\
    .set_start_mode_cls(mode.ModeOpening0)\
    .set_state_cls(State)\
    .set_src_directory(constants.SRC_DIRECTORY)\
    .set_screen_size(constants.SCREEN_SIZE)\
    .set_title(constants.TITLE)\
    .set_window_icon(constants.WINDOW_ICON)\
    .set_event_names(constants.EVENT_NAMES)\
    .set_input_defaults(constants.INPUT_DEFAULTS)\
    .set_font_location(constants.FONT)\
    .set_font_size(constants.FONT_SIZE)\
    .set_font_height(constants.FONT_HEIGHT)\
    .set_font_antialias(constants.FONT_ANTIALIAS)\
    .build()
while game.run():
    pass

sys.exit()
