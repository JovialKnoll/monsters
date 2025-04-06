import sys
import os

import jovialengine
import pygame

TITLE = "CHIKKAI! Tiny Kaijus"
SCREEN_SIZE = (320, 180)
COLORKEY = (255, 0, 255)
FONT_SIZE = 8
FONT_HEIGHT = 10
FONT_ANTIALIAS = False

EVENT_NAMES = (
    "Left",
    "Right",
    "Up",
    "Down",
    "Confirm",
)
EVENT_LEFT = jovialengine.EVENT_TYPE_START_POS
EVENT_RIGHT = jovialengine.EVENT_TYPE_START_POS + 1
EVENT_UP = jovialengine.EVENT_TYPE_START_POS + 2
EVENT_DOWN = jovialengine.EVENT_TYPE_START_POS + 3
EVENT_CONFIRM = jovialengine.EVENT_TYPE_START_POS + 4
ALL_EVENTS = {
    EVENT_LEFT,
    EVENT_RIGHT,
    EVENT_UP,
    EVENT_DOWN,
    EVENT_CONFIRM,
}
INPUT_DEFAULTS = (
    jovialengine.InputDefault(0, EVENT_LEFT, jovialengine.InputType.KEYBOARD, pygame.K_LEFT),
    jovialengine.InputDefault(0, EVENT_RIGHT, jovialengine.InputType.KEYBOARD, pygame.K_RIGHT),
    jovialengine.InputDefault(0, EVENT_UP, jovialengine.InputType.KEYBOARD, pygame.K_UP),
    jovialengine.InputDefault(0, EVENT_DOWN, jovialengine.InputType.KEYBOARD, pygame.K_DOWN),
    jovialengine.InputDefault(0, EVENT_CONFIRM, jovialengine.InputType.KEYBOARD, pygame.K_RETURN),
    jovialengine.InputDefault(0, EVENT_LEFT, jovialengine.InputType.KEYBOARD, pygame.K_a),
    jovialengine.InputDefault(0, EVENT_RIGHT, jovialengine.InputType.KEYBOARD, pygame.K_d),
    jovialengine.InputDefault(0, EVENT_UP, jovialengine.InputType.KEYBOARD, pygame.K_w),
    jovialengine.InputDefault(0, EVENT_DOWN, jovialengine.InputType.KEYBOARD, pygame.K_s),
    jovialengine.InputDefault(0, EVENT_LEFT, jovialengine.InputType.CON_HAT, 0),
    jovialengine.InputDefault(0, EVENT_RIGHT, jovialengine.InputType.CON_HAT, 1),
    jovialengine.InputDefault(0, EVENT_UP, jovialengine.InputType.CON_HAT, 2),
    jovialengine.InputDefault(0, EVENT_DOWN, jovialengine.InputType.CON_HAT, 3),
    jovialengine.InputDefault(0, EVENT_CONFIRM, jovialengine.InputType.CON_BUTTON, 0),
)

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
TITLE_PLAY = os.path.join(MUSIC_DIRECTORY, 'title_play.ogg')
CHAT_LOOP = os.path.join(MUSIC_DIRECTORY, 'chat_loop.ogg')
FIGHT_LOOP = os.path.join(MUSIC_DIRECTORY, 'fight_loop.ogg')
CREDITS_PLAY = os.path.join(MUSIC_DIRECTORY, 'credits.ogg')

IMAGE_DIRECTORY = os.path.join(SRC_DIRECTORY, 'images')

CREDITS_TEXT = os.path.join(TEXT_DIRECTORY, 'credits.txt')
CONVO_DIRECTORY = os.path.join(TEXT_DIRECTORY, 'convos')

VERSION_TEXT = os.path.join(ASSETS_DIRECTORY, 'version.txt')
VERSION = ''
try:
    with open(VERSION_TEXT) as version_file:
        VERSION = version_file.readline().rstrip('\n')
except FileNotFoundError:
    pass
