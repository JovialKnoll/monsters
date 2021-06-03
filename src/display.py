import os

import pygame

import constants
import shared


class Display(object):
    __slots__ = (
        '_monitor_res',
        '_upscale_max',
        '_windowed_flags',
        '_fullscreen_flags',
        'is_fullscreen',
        'upscale',
        '_disp_res',
        'screen',
        '_fullscreen_offset',
        '_full_screen',
        '_disp_screen',
    )

    def __init__(self):
        self._setupDisplay()
        self.is_fullscreen = shared.config.getboolean(constants.CONFIG_SECTION, constants.CONFIG_FULLSCREEN)
        self.upscale = shared.config.getint(constants.CONFIG_SECTION, constants.CONFIG_SCREEN_SCALE)
        self.upscale = max(min(self.upscale, self._upscale_max), 0)
        self._scaleDisp()
        self.screen = pygame.Surface(constants.SCREEN_SIZE)
        self._fullscreen_offset = None
        self._full_screen = None
        if self.is_fullscreen:
            self._setFullscreen()
        else:
            self._setWindowed()
        self.screen = self.screen.convert(self._disp_screen)
        shared.config.set(constants.CONFIG_SECTION, constants.CONFIG_SCREEN_SCALE, str(self.upscale))

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
        max_disp_res = (
            constants.SCREEN_SIZE[0] * self._upscale_max,
            constants.SCREEN_SIZE[1] * self._upscale_max,
        )
        self._windowed_flags = 0
        if pygame.display.mode_ok(max_disp_res, pygame.DOUBLEBUF):
            self._windowed_flags = pygame.DOUBLEBUF
        self._fullscreen_flags = 0
        if pygame.display.mode_ok(self._monitor_res, pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE):
            self._fullscreen_flags = pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE
        elif pygame.display.mode_ok(self._monitor_res, pygame.FULLSCREEN | pygame.DOUBLEBUF):
            self._fullscreen_flags = pygame.FULLSCREEN | pygame.DOUBLEBUF
        elif pygame.display.mode_ok(self._monitor_res, pygame.FULLSCREEN):
            self._fullscreen_flags = pygame.FULLSCREEN

    def changeScale(self, scale_change: int):
        new_scale = self.upscale + scale_change
        if new_scale < 1 or new_scale > self._upscale_max:
            return
        self._alterScale(new_scale)

    def setScale(self, target_scale: int):
        new_scale = min(target_scale, self._upscale_max)
        if new_scale == self.upscale:
            return
        self._alterScale(new_scale)

    def _alterScale(self, new_scale: int):
        self.upscale = new_scale
        self._scaleDisp()
        if self.is_fullscreen:
            self._setFullscreen()
        else:
            pygame.display.quit()
            pygame.display.init()
            self._setupDisplay()
            self._setWindowed()
        self.screen = self.screen.convert(self._disp_screen)
        shared.config.set(constants.CONFIG_SECTION, constants.CONFIG_SCREEN_SCALE, str(self.upscale))

    def _scaleDisp(self):
        self._disp_res = (
            constants.SCREEN_SIZE[0] * self.upscale,
            constants.SCREEN_SIZE[1] * self.upscale,
        )

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
            self._windowed_flags
        )

    def _setFullscreen(self):
        self._fullscreen_offset = (
            (self._monitor_res[0] - self._disp_res[0]) // 2,
            (self._monitor_res[1] - self._disp_res[1]) // 2,
        )
        if self._full_screen is None:
            self._full_screen = pygame.display.set_mode(
                self._monitor_res,
                self._fullscreen_flags
            )
        else:
            self._full_screen.fill(constants.BLACK)
        self._disp_screen = pygame.Surface(self._disp_res).convert(self._full_screen)

    def scaleMouseInput(self, event: pygame.event.Event):
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
