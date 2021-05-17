import os

import pygame

import constants
import shared


class Display(object):
    __slots__ = (
        '_monitor_res',
        '_upscale_max',
        'screen',
        'is_fullscreen',
        'upscale',
        '_disp_res',
        '_fullscreen_offset',
        '_disp_screen',
        '_full_screen',
    )

    def __init__(self):
        self._setupDisplay()
        self.is_fullscreen = shared.config.getboolean(constants.CONFIG_SECTION, constants.CONFIG_FULLSCREEN)
        self.upscale = shared.config.getint(constants.CONFIG_SECTION, constants.CONFIG_SCREEN_SCALE)
        self.upscale = max(min(self.upscale, self._upscale_max), 0)
        shared.config.set(constants.CONFIG_SECTION, constants.CONFIG_SCREEN_SCALE, str(self.upscale))
        self.screen = pygame.Surface(constants.SCREEN_SIZE)
        if self.is_fullscreen:
            self._setFullscreen()
        else:
            self._scaleWindow()

    def _setupDisplay(self):
        pygame.display.set_caption(constants.SCREEN_CAPTION)
        # todo: set window icon here
        # todo: replace with a custom mouse icon or get rid of it?
        # pygame.mouse.set_visible(False)
        display_info = pygame.display.Info()
        self._monitor_res = (
            display_info.current_w,
            display_info.current_h,
        )
        self._upscale_max = min(
            self._monitor_res[0] // constants.SCREEN_SIZE[0],
            self._monitor_res[1] // constants.SCREEN_SIZE[1]
        )

    def changeScale(self, scale_change):
        if not self.is_fullscreen:
            new_upscale = self.upscale + scale_change
            if new_upscale < 1 or new_upscale > self._upscale_max:
                return
            self.upscale = new_upscale
            pygame.display.quit()
            self._scaleWindow()

    def _scaleWindow(self):
        """Set the window to a new scale."""

        self._disp_res = (
            constants.SCREEN_SIZE[0] * self.upscale,
            constants.SCREEN_SIZE[1] * self.upscale,
        )
        # center window
        os.environ['SDL_VIDEO_WINDOW_POS'] = "{},{}".format(
            (self._monitor_res[0] - self._disp_res[0]) // 2,
            (self._monitor_res[1] - self._disp_res[1]) // 2
        )
        pygame.display.init()
        self._setupDisplay()
        self._disp_screen = pygame.display.set_mode(
            self._disp_res,
            pygame.DOUBLEBUF
        )
        self.screen = self.screen.convert(self._disp_screen)
        self.is_fullscreen = False
        shared.config.set(constants.CONFIG_SECTION, constants.CONFIG_SCREEN_SCALE, str(self.upscale))

    def toggleFullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        pygame.display.quit()
        pygame.display.init()
        self._setupDisplay()
        if self.is_fullscreen:
            self._setFullscreen()
        else:
            self._setWindowed()
        self.screen = self.screen.convert(self._disp_screen)
        shared.config.set(constants.CONFIG_SECTION, constants.CONFIG_FULLSCREEN, str(self.is_fullscreen))

    def _setWindowed(self):
        # center window
        os.environ['SDL_VIDEO_WINDOW_POS'] = "{},{}".format(
            (self._monitor_res[0] - self._disp_res[0]) // 2,
            (self._monitor_res[1] - self._disp_res[1]) // 2
        )
        self._fullscreen_offset = None
        self._full_screen = None
        self._disp_screen = pygame.display.set_mode(
            self._disp_res,
            pygame.DOUBLEBUF
        )

    def _setFullscreen(self):
        self._fullscreen_offset = (
            (self._monitor_res[0] - self._disp_res[0]) // 2,
            (self._monitor_res[1] - self._disp_res[1]) // 2,
        )
        self._full_screen = pygame.display.set_mode(
            self._monitor_res,
            pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE
        )
        self._disp_screen = pygame.Surface(self._disp_res).convert(self._full_screen)

    def scaleMouseInput(self, event):
        """Scale mouse position for events in terms of the screen (as opposed to the display surface)."""
        if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):
            if self.is_fullscreen:
                event_dict = {
                    'pos': (
                        (event.pos[0] - self._fullscreen_offset[0]) // self.upscale,
                        (event.pos[1] - self._fullscreen_offset[1]) // self.upscale,
                    )
                }
            else:
                event_dict = {
                    'pos': (
                        event.pos[0] // self.upscale,
                        event.pos[1] // self.upscale,
                    )
                }
            if event.type == pygame.MOUSEMOTION:
                event_dict['rel'] = (
                    event.rel[0] // self.upscale,
                    event.rel[1] // self.upscale,
                )
                event_dict['buttons'] = event.buttons
            else:
                event_dict['button'] = event.button
            return pygame.event.Event(event.type, event_dict)
        return event

    def scaleDraw(self):
        """Scale screen onto display surface, then flip the display."""
        pygame.transform.scale(self.screen, self._disp_res, self._disp_screen)
        if self.is_fullscreen:
            self._full_screen.blit(self._disp_screen, self._fullscreen_offset)
        pygame.display.flip()
