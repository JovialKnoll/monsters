import pygame
import constants

from fontwrap import *
from monster import *

class SharedState(object):
    __slots__ = (
        'font_wrap',
        'screen',
        'protag_mon',
    )

    def _setup(self):
        pygame.init()
        font = pygame.font.Font(constants.FONT_FILE, constants.FONT_SIZE)
        self.font_wrap = FontWrap(font)
        self.screen = pygame.Surface(constants.SCREEN_SIZE)

    def __init__(self):
        self._setup()
        self.protag_mon = Monster()

state = SharedState()
