import configparser

import constants
from fontwrap import FontWrap
from display import Display
from state import State


config = configparser.ConfigParser(constants.CONFIG_DEFAULTS, default_section=constants.CONFIG_SECTION)
config.read(constants.CONFIG_FILE)
for section in config.sections():
    config.remove_section(section)
font_wrap = FontWrap(constants.FONT, constants.FONT_SIZE)
display = Display()
state = State()
game_running = True
