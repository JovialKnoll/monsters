import os

SCREEN_CAPTION = "Monsters and Stuff"
SCREEN_SIZE = (320, 180)
MAX_FRAMERATE = 60
CURSOR_TIME = 20
FONT_SIZE = 8
TEXT_COLOR = (164, 162, 165)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

GRAPHICS_DIRECTORY = 'gfx'
FONT_FILE = os.path.join(GRAPHICS_DIRECTORY, 'simple_mono.ttf')

BACKGROUNDS_DIRECTORY = os.path.join(GRAPHICS_DIRECTORY, 'backgrounds')
BLACKBOX_FILE = os.path.join(BACKGROUNDS_DIRECTORY, 'blackbox.png')
HEALTHBAR_FILE = os.path.join(BACKGROUNDS_DIRECTORY, 'healthbar.png')
LAYOUT_1_FILE = os.path.join(BACKGROUNDS_DIRECTORY, 'layout1boxes.png')
LAYOUT_2_FILE = os.path.join(BACKGROUNDS_DIRECTORY, 'layout2boxes.png')

MONSTER_PARTS_DIRECTORY = os.path.join(GRAPHICS_DIRECTORY, 'monster-parts')

SAVE_DIRECTORY = 'savegames'
