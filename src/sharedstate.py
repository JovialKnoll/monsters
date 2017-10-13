import pygame

from constants import *
from fontwrap import *
from monster import *

class SharedState(object):
    def __init__(self):
        font = pygame.font.Font(os.path.join(GRAPHICS_DIRECTORY, FONT_FILE), FONT_SIZE)
        self.font_wrap = FontWrap(font)
        self.protag_mon = Monster()
