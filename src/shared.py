import os

import pygame

import constants
from fontwrap import FontWrap

pygame.init()
game_running = True
font_wrap = FontWrap(
    pygame.font.Font(constants.FONT_FILE, constants.FONT_SIZE)
)
# display stuff
pygame.display.set_caption(constants.SCREEN_CAPTION)
# set window icon here
# replace with a custom mouse icon or get rid of it?
# pygame.mouse.set_visible(False)
monitor_res = (
    pygame.display.Info().current_w,
    pygame.display.Info().current_h,
)
upscale_max = min(
    monitor_res[0] // constants.SCREEN_SIZE[0],
    monitor_res[1] // constants.SCREEN_SIZE[1]
)
disp_res_max = (
    constants.SCREEN_SIZE[0] * upscale_max,
    constants.SCREEN_SIZE[1] * upscale_max,
)
fullscreen_offset = (
    (monitor_res[0] - disp_res_max[0]) // 2,
    (monitor_res[1] - disp_res_max[1]) // 2,
)
upscale = upscale_max // 2
disp_res = None
is_fullscreen = None
# screens
disp_screen = None
full_screen = pygame.Surface(disp_res_max)
screen = pygame.Surface(constants.SCREEN_SIZE)

def screenSet(scale_change):
    """Set the window to a new scale."""
    global upscale
    global disp_res
    global disp_screen
    global screen
    global is_fullscreen
    new_upscale = upscale + scale_change
    if new_upscale < 1 or new_upscale > upscale_max:
        return
    upscale = new_upscale
    disp_res = (
        constants.SCREEN_SIZE[0] * upscale,
        constants.SCREEN_SIZE[1] * upscale,
    )
    disp_screen = pygame.display.set_mode(disp_res)
    screen = screen.convert(disp_screen)
    # center window
    if os.name == 'nt':
        os.environ['SDL_VIDEO_WINDOW_POS'] = "{},{}".format(
            (monitor_res[0] - disp_res[0]) // 2,
            (monitor_res[1] - disp_res[1]) // 2
        )
    is_fullscreen = False

def screenSetFullscreen():
    """Set the window to fullscreen."""
    global disp_screen
    global full_screen
    global screen
    global is_fullscreen
    disp_screen = pygame.display.set_mode(monitor_res, pygame.FULLSCREEN)
    # needs a separate full screen in case the largest full-multiple scale-up doesn't fit
    full_screen = full_screen.convert(disp_screen)
    screen = screen.convert(full_screen)
    is_fullscreen = True

screenSet(0)
