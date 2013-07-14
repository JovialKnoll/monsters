import pygame, os, sys
from fontwrap import *
from gamemode import *
from quitmode import *

from testmode import *
from convomode0 import *
class Game(object):
    def __init__(self):
        """Start and create things as needed."""
        pygame.init()
        self.running = True
        #pygame.mouse.set_visible(False)
        #set window icon/captions here...
        GameMode.shared = {'SCREEN_SIZE': (320,180), 'font': pygame.font.Font(os.path.join('gfx', 'simple_mono.ttf'), 8)}
        GameMode.shared['font_wrap'] = FontWrap(GameMode.shared['font'])
        #all children of GameMode can access the shared dictionary with self.shared
        self.screen = pygame.Surface(GameMode.shared['SCREEN_SIZE'])
        self.monitor_res = (pygame.display.Info().current_w,pygame.display.Info().current_h)
        self.upscale_max = min(self.monitor_res[0]//GameMode.shared['SCREEN_SIZE'][0], self.monitor_res[1]//GameMode.shared['SCREEN_SIZE'][1])
        self.upscale = self.upscale_max//2
        self.disp_res_max = (GameMode.shared['SCREEN_SIZE'][0]*self.upscale_max, GameMode.shared['SCREEN_SIZE'][1]*self.upscale_max)
        self._windowSet(0)
        self.fullscreen_offset = ((self.monitor_res[0]-self.disp_res_max[0])//2, (self.monitor_res[1]-self.disp_res_max[1])//2)
        self.full_screen = pygame.Surface(self.disp_res_max)
        self.framerate = 60
        self.clock = pygame.time.Clock()
        
        self.quit_mode = False
        self.current_mode = False
        
        #test stuff
        #self.current_mode = TestMode()
        self.current_mode = ConvoMode0()
        
    def __del__(self):
        """End and delete things as needed."""
        pygame.quit()
        
    def _windowSet(self, scale_change):
        """Set the window to a scale of upscale + scale_change."""
        self.upscale += scale_change
        self.disp_res = (GameMode.shared['SCREEN_SIZE'][0]*self.upscale, GameMode.shared['SCREEN_SIZE'][1]*self.upscale)
        if not sys.platform.startswith('freebsd') and not sys.platform.startswith('darwin'):
            os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % ((self.monitor_res[0]-self.disp_res[0])//2, (self.monitor_res[1]-self.disp_res[1])//2)
        self.disp_screen = pygame.display.set_mode(self.disp_res)
        self.screen.convert()
        self.is_fullscreen = False
        
    def _windowSetFullscreen(self):
        """Set the window to fullscreen."""
        self.disp_screen = pygame.display.set_mode(self.monitor_res, pygame.FULLSCREEN)
        self.full_screen.convert()
        self.screen.convert(self.full_screen)
        self.is_fullscreen = True
        
    def _saveGame(self):
        """Save the game."""
        pass#a blank function for now
        
    def run(self):
        """Run the game, and check if the game needs to end."""
        if not self.running:
            return False
        self.event_list = self._filterInput(pygame.event.get())
        if self.quit_mode:
            self.quit_mode.input(self.event_list)
            self.quit_mode.update()
            self.quit_mode.draw(self.screen)
            if self.quit_mode.choice == 1:
                self.quit_mode = False
            elif self.quit_mode.choice == 2:
                self._saveGame()
                self.running = False
            elif self.quit_mode.choice == 3:
                self.running = False
                
        elif self.current_mode:
            self.current_mode.input(self.event_list)
            self.current_mode.update()
            self.current_mode.draw(self.screen)
            if self.current_mode.next_mode != False:
                self.current_mode = self.current_mode.next_mode
                
        else:
            self._input(self.event_list)
            self._update()
            self._draw(self.screen)
        self._scaleThings()
        self._time()
        return True
        
    def _stillNeedsHandling(self, event):
        """If event should be handled before all others, handle it and return False, otherwise return True.
        As an example, game-ending or display-changing events should be handled before all others.
        """
        if event.type == pygame.QUIT:
            if self.quit_mode:
                self.running = False
            else:
                self.quit_mode = QuitMode()
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.quit_mode:
                    self.running = False
                else:
                    self.quit_mode = QuitMode()
                return False
            #Window re-sizing stuff
            elif event.key == pygame.K_PAGEUP or event.key == pygame.K_PERIOD:
                if self.upscale < self.upscale_max:
                    self._windowSet(1)
                return False
            elif event.key == pygame.K_PAGEDOWN or event.key == pygame.K_COMMA:
                if self.upscale > 1:
                    self._windowSet(-1)
                return False
            elif event.key == pygame.K_F11 or event.key == pygame.K_TAB:
                if self.is_fullscreen:
                    self._windowSet(0)
                else:
                    self._windowSetFullscreen()
                return False
        return True
        
    def _scaleMouseInput(self, event):
        """Scale mouse position for events in terms of the screen (as opposed to the display surface)."""
        if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_fullscreen:
                event_dict = {'pos': ((event.pos[0]-self.fullscreen_offset[0])//self.upscale_max, (event.pos[1]-self.fullscreen_offset[1])//self.upscale_max)}#good?
            else:
                event_dict = {'pos': (event.pos[0]//self.upscale, event.pos[1]//self.upscale)}
            if event.type == pygame.MOUSEMOTION:
                event_dict['rel'] = event.rel
                event_dict['buttons'] = event.buttons
            else:
                event_dict['button'] = event.button
            return pygame.event.Event(event.type, event_dict)
        return event
        
    def _filterInput(self, events):
        """Take care of input that game modes should not take care of."""
        return map(self._scaleMouseInput, filter(self._stillNeedsHandling, events))
        
    def _input(self, event_list):
        """Take inputs as needed."""
        pass
        
    def _update(self):
        """Update things as needed."""
        pass
        
    def _draw(self, screen):
        """Draw things as needed."""
        pass
        
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
        pygame.display.set_caption(str(self.clock.get_fps()))
        self.clock.tick(self.framerate)
        