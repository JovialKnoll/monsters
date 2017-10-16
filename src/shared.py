import pygame
import constants

from fontwrap import *

pygame.init()
font_wrap = FontWrap(
    pygame.font.Font(constants.FONT_FILE, constants.FONT_SIZE)
)
screen = pygame.Surface(constants.SCREEN_SIZE)
# other display stuff held by game goes here
