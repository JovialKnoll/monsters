import os

import pygame

import constants
from display import Display
from fontwrap import FontWrap
from state import State

game_running = True
display = Display()
font_wrap = FontWrap(
    pygame.font.Font(constants.FONT_FILE, constants.FONT_SIZE)
)
state = State()
