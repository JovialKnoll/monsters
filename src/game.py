import pygame, sys, os
from constants import *
from fontwrap import *
from gamemode import *
from gamemenumode import *

from monster import *

from testmode import *
from convomode0 import *
class Game(object):
    def __init__(self):
        """Start and create things as needed."""
        pygame.init()
        self.running = True
        #pygame.mouse.set_visible(False)
        #set window icon/captions here...
        font = pygame.font.Font(os.path.join(GRAPHICS_DIRECTORY, FONT_FILE), FONT_SIZE)
        GameMode.shared = { 'font_wrap': FontWrap(font) }
        #all children of GameMode can access the shared dictionary with self.shared

        #space
        self.screen = pygame.Surface(SCREEN_SIZE)
        self.monitor_res = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        self.upscale_max = min(self.monitor_res[0]//SCREEN_SIZE[0], self.monitor_res[1]//SCREEN_SIZE[1])
        self.upscale = self.upscale_max//2
        self.disp_res_max = (SCREEN_SIZE[0]*self.upscale_max, SCREEN_SIZE[1]*self.upscale_max)
        self._windowSet(0)
        self.fullscreen_offset = ((self.monitor_res[0]-self.disp_res_max[0])//2, (self.monitor_res[1]-self.disp_res_max[1])//2)
        self.full_screen = pygame.Surface(self.disp_res_max)

        #time
        self.clock = pygame.time.Clock()

        self.current_menu = False
        self.current_mode = False

        GameMode.shared['protag_mon'] = Monster()

        #test stuff
        #self.current_mode = TestMode()
        self.current_mode = ConvoMode0()

    def __del__(self):
        """End and delete things as needed."""
        pygame.quit()

    def _windowSet(self, scale_change):
        """Set the window to a scale of upscale + scale_change."""
        self.upscale += scale_change
        self.disp_res = (SCREEN_SIZE[0]*self.upscale, SCREEN_SIZE[1]*self.upscale)
        if not sys.platform.startswith('freebsd') and not sys.platform.startswith('darwin'):
            os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % ((self.monitor_res[0]-self.disp_res[0])//2, (self.monitor_res[1]-self.disp_res[1])//2)
        self.disp_screen = pygame.display.set_mode(self.disp_res)
        self.screen = self.screen.convert()
        self.is_fullscreen = False

    def _windowSetFullscreen(self):
        """Set the window to fullscreen."""
        self.disp_screen = pygame.display.set_mode(self.monitor_res, pygame.FULLSCREEN)
        self.full_screen = self.full_screen.convert()
        self.screen = self.screen.convert(self.full_screen)
        self.is_fullscreen = True

    def run(self):
        """Run the game, and check if the game needs to end."""
        if not self.running:
            return False
        event_list = self._filterInput(pygame.event.get())
        mode = self.current_mode
        if self.current_menu:
            mode = self.current_menu
        if mode:
            mode.input(event_list)
            mode.update()
            mode.draw(self.screen)
            if mode.next_mode != False:
                self.current_mode = mode.next_mode
        else:
            #put something here for a no mode / ready to load game screen
            pass
        self._scaleThings()
        self._time()
        return True

    def _filterInput(self, events):
        """Take care of input that game modes should not take care of."""
        return map(self._scaleMouseInput, filter(self._stillNeedsHandling, events))

    def _handleQuit(self):
        if self.current_menu is False:
            self.current_menu = GameMenuMode()
            return False
        return True

    def _stillNeedsHandling(self, event):
        """If event should be handled before all others, handle it and return False, otherwise return True.
        As an example, game-ending or display-changing events should be handled before all others.
        """
        if event.type == pygame.QUIT:
            return self._handleQuit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return self._handleQuit()
            #window re-sizing stuff
            elif event.key in (pygame.K_PAGEUP, pygame.K_PERIOD):
                if self.upscale < self.upscale_max:
                    self._windowSet(1)
                return False
            elif event.key in (pygame.K_PAGEDOWN, pygame.K_COMMA):
                if self.upscale > 1:
                    self._windowSet(-1)
                return False
            elif event.key in (pygame.K_F11, pygame.K_TAB):
                if self.is_fullscreen:
                    self._windowSet(0)
                else:
                    self._windowSetFullscreen()
                return False
        return True

    def _scaleMouseInput(self, event):
        """Scale mouse position for events in terms of the screen (as opposed to the display surface)."""
        if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):
            if self.is_fullscreen:
                event_dict = {'pos': ((event.pos[0]-self.fullscreen_offset[0])//self.upscale_max, (event.pos[1]-self.fullscreen_offset[1])//self.upscale_max)}
            else:
                event_dict = {'pos': (event.pos[0]//self.upscale, event.pos[1]//self.upscale)}
            if event.type == pygame.MOUSEMOTION:
                event_dict['rel'] = event.rel
                event_dict['buttons'] = event.buttons
            else:
                event_dict['button'] = event.button
            return pygame.event.Event(event.type, event_dict)
        return event

    def _scaleThings(self):
        """Scale screen onto display surface, then flip the display."""
        if not self.is_fullscreen:
            pygame.transform.scale(self.screen, self.disp_res, self.disp_screen)
        else:
            pygame.transform.scale(self.screen, self.disp_res_max, self.full_screen)
            self.disp_screen.blit(self.full_screen, self.fullscreen_offset)
        pygame.display.flip()

    def _time(self):
        """Take care of time stuff."""
        pygame.display.set_caption(str(self.clock.get_fps()))#just for debugging purposes
        self.clock.tick(FRAMERATE)
