import os
import random

import constants
from display import Display
from fontwrap import FontWrap
from state import State

random.seed()
game_running = True
display = Display()
font_wrap = FontWrap(constants.FONT_FILE, constants.FONT_SIZE)
state = State()
