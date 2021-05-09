import configparser

import constants
from fontwrap import FontWrap
from display import Display
from state import State

config = configparser.ConfigParser(constants.CONFIG_DEFAULTS)
config.add_section(constants.CONFIG_SECTION)
config.read(constants.CONFIG_FILE)
font_wrap = FontWrap(constants.FONT, constants.FONT_SIZE)
display = Display()
state = State()
game_running = True
