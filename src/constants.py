import os

import pygame

SCREEN_CAPTION = "CHIKKAI!"
SCREEN_SIZE = (320, 180)
SCREEN_RECT = pygame.Rect((0, 0), SCREEN_SIZE)
CURSOR_TIME = 500
FONT_SIZE = 8
FONT_HEIGHT = 10
TEXT_COLOR = (164, 162, 165)
DARK_TEXT_COLOR = (82, 81, 83)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORKEY = (255, 0, 255)

GRAPHICS_DIRECTORY = 'gfx'
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

SOUND_DIRECTORY = 'sfx'
THUNK = os.path.join(SOUND_DIRECTORY, 'thunk.wav')
SPROING = os.path.join(SOUND_DIRECTORY, 'sproing.wav')
FSSSH = os.path.join(SOUND_DIRECTORY, 'fsssh.wav')
BIP = os.path.join(SOUND_DIRECTORY, 'bip.wav')
LONGSLIDE = os.path.join(SOUND_DIRECTORY, 'longslide.wav')
ROOEEE = os.path.join(SOUND_DIRECTORY, 'rooeee.wav')
BWOP = os.path.join(SOUND_DIRECTORY, 'bwop.wav')

MUSIC_DIRECTORY = os.path.join(SOUND_DIRECTORY, 'music')
FIGHT_LOOP = os.path.join(MUSIC_DIRECTORY, 'fight_loop.ogg')

SAVE_DIRECTORY = 'saves'

CONFIG_FILE = 'config.ini'
CONFIG_SECTION = 'Game'
CONFIG_MAX_FRAMERATE = 'MaxFramerate'
CONFIG_FULLSCREEN = 'Fullscreen'
CONFIG_SCREEN_SCALE = 'ScreenScale'
CONFIG_DEFAULTS = {
    CONFIG_MAX_FRAMERATE: 60,
    CONFIG_FULLSCREEN: False,
    CONFIG_SCREEN_SCALE: 4,
}
