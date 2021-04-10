import os

SCREEN_CAPTION = "Monsters and Stuff"
SCREEN_SIZE = (320, 180)
CURSOR_TIME = 500
FONT_SIZE = 8
FONT_HEIGHT = 10
TEXT_COLOR = (164, 162, 165)
DARK_TEXT_COLOR = (82, 81, 83)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORKEY = (255, 0, 255)

GRAPHICS_DIRECTORY = 'gfx'
FONT_FILE = os.path.join(GRAPHICS_DIRECTORY, 'simple_mono.ttf')
JK_LOGO_BLACK = os.path.join(GRAPHICS_DIRECTORY, 'jklogo_black.png')
JK_LOGO_GREY = os.path.join(GRAPHICS_DIRECTORY, 'jklogo_grey.png')
JK_LOGO_LIGHT_GREY = os.path.join(GRAPHICS_DIRECTORY, 'jklogo_light_grey.png')
STAR = os.path.join(GRAPHICS_DIRECTORY, 'star.png')

BACKGROUNDS_DIRECTORY = os.path.join(GRAPHICS_DIRECTORY, 'backgrounds')
BLACKBOX_FILE = os.path.join(BACKGROUNDS_DIRECTORY, 'blackbox.png')
HEALTHBAR_FILE = os.path.join(BACKGROUNDS_DIRECTORY, 'healthbar.png')
LAYOUT_1_FILE = os.path.join(BACKGROUNDS_DIRECTORY, 'layout1boxes.png')
LAYOUT_2_FILE = os.path.join(BACKGROUNDS_DIRECTORY, 'layout2boxes.png')

MONSTER_PARTS_DIRECTORY = os.path.join(GRAPHICS_DIRECTORY, 'monster-parts')

SAVE_DIRECTORY = 'savegames'
