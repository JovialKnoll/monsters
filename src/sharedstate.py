import pygame
import constants

from fontwrap import *
from monster import *

pygame.init()
font_wrap = FontWrap(
    pygame.font.Font(constants.FONT_FILE, constants.FONT_SIZE)
)
screen = pygame.Surface(constants.SCREEN_SIZE)

class SharedState(object):
    __slots__ = (
        'protag_mon',
    )

    def __init__(self):
        self.protag_mon = Monster()

state = SharedState()
