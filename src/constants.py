import sys
import os


TITLE = "CHIKKAI! Tiny Kaijus"
SCREEN_SIZE = (320, 180)
COLORKEY = (255, 0, 255)
FONT_SIZE = 8
FONT_HEIGHT = 10

TEXT_COLOR = (164, 162, 165)
DARK_TEXT_COLOR = (82, 81, 83)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

FIGHT_ATTACK = "Aggressive Attack"
FIGHT_DEFEND = "Defensive Attack"
FIGHT_DODGE = "Dodge"

_location = '.'
if getattr(sys, 'frozen', False):
    _location = sys.executable
elif __file__:
    _location = __file__
SRC_DIRECTORY = os.path.dirname(_location)

ASSETS_DIRECTORY = os.path.join(SRC_DIRECTORY, 'assets')
GRAPHICS_DIRECTORY = os.path.join(ASSETS_DIRECTORY, 'gfx')
SOUND_DIRECTORY = os.path.join(ASSETS_DIRECTORY, 'sfx')
TEXT_DIRECTORY = os.path.join(ASSETS_DIRECTORY, 'txt')
SAVE_DIRECTORY = os.path.join(SRC_DIRECTORY, 'saves')
SCREENSHOT_DIRECTORY = os.path.join(SRC_DIRECTORY, 'screenshots')

CONFIG_FILE = os.path.join(SRC_DIRECTORY, 'config.ini')
WINDOW_ICON = os.path.join(GRAPHICS_DIRECTORY, 'icon.png')
FONT = os.path.join(GRAPHICS_DIRECTORY, 'simple_mono.ttf')

LOGOS_DIRECTORY = os.path.join(GRAPHICS_DIRECTORY, 'logos')
JK_LOGO_BLACK = os.path.join(LOGOS_DIRECTORY, 'jklogo_black.png')
JK_LOGO_GREY = os.path.join(LOGOS_DIRECTORY, 'jklogo_grey.png')
JK_LOGO_LIGHT_GREY = os.path.join(LOGOS_DIRECTORY, 'jklogo_light_grey.png')
STAR = os.path.join(LOGOS_DIRECTORY, 'star.png')
TIN_LOGO = os.path.join(LOGOS_DIRECTORY, 'tin_logo.png')
CHIKKAI_LOGO = os.path.join(LOGOS_DIRECTORY, 'chikkai_logo.png')

BACKGROUNDS_DIRECTORY = os.path.join(GRAPHICS_DIRECTORY, 'backgrounds')
BLACKBOX_FILE = os.path.join(BACKGROUNDS_DIRECTORY, 'blackbox.png')
HEALTHBAR_FILE = os.path.join(BACKGROUNDS_DIRECTORY, 'healthbar.png')
LAYOUT_1_FILE = os.path.join(BACKGROUNDS_DIRECTORY, 'layout1boxes.png')
LAYOUT_2_FILE = os.path.join(BACKGROUNDS_DIRECTORY, 'layout2boxes.png')

MONSTER_PARTS_DIRECTORY = os.path.join(GRAPHICS_DIRECTORY, 'monster-parts')

THUNK = os.path.join(SOUND_DIRECTORY, 'thunk.ogg')
SPROING = os.path.join(SOUND_DIRECTORY, 'sproing.ogg')
FSSSH = os.path.join(SOUND_DIRECTORY, 'fsssh.ogg')
BIP = os.path.join(SOUND_DIRECTORY, 'bip.ogg')
LONGSLIDE = os.path.join(SOUND_DIRECTORY, 'longslide.ogg')
ROOEEE = os.path.join(SOUND_DIRECTORY, 'rooeee.ogg')
BWOP = os.path.join(SOUND_DIRECTORY, 'bwop.ogg')

MUSIC_DIRECTORY = os.path.join(SOUND_DIRECTORY, 'music')
TITLE_INTRO = os.path.join(MUSIC_DIRECTORY, 'title_intro.ogg')
CHAT_LOOP = os.path.join(MUSIC_DIRECTORY, 'chat_loop.ogg')
FIGHT_LOOP = os.path.join(MUSIC_DIRECTORY, 'fight_loop.ogg')

IMAGE_DIRECTORY = os.path.join(SRC_DIRECTORY, 'images')

VERSION_TEXT = os.path.join(TEXT_DIRECTORY, 'version.txt')
CREDITS_TEXT = os.path.join(TEXT_DIRECTORY, 'credits.txt')
CONVO_DIRECTORY = os.path.join(TEXT_DIRECTORY, 'convos')

VERSION = ''
try:
    with open(VERSION_TEXT) as version_file:
        VERSION = version_file.readline().rstrip('\n')
except FileNotFoundError:
    pass
