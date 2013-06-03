import pygame, os, sys
from testmode import *
class Game(object):
    def __init__(self):
        """Start and create things as needed."""
        pygame.init()
        self.running = True
        pygame.mouse.set_visible(False)
        #set window icon/captions here...
        self.SCREEN_SIZE = (320,180)
        self.screen = pygame.Surface(self.SCREEN_SIZE)
        self.monitor_res = (pygame.display.Info().current_w,pygame.display.Info().current_h)
        self.upscale_max = min(self.monitor_res[0]//self.SCREEN_SIZE[0], self.monitor_res[1]//self.SCREEN_SIZE[1])
        self.upscale = self.upscale_max//2
        self.disp_res_max = (self.SCREEN_SIZE[0]*self.upscale_max, self.SCREEN_SIZE[1]*self.upscale_max)
        self.windowSet(0)
        self.fullscreen_offset = ((self.monitor_res[0]-self.disp_res_max[0])/2, (self.monitor_res[1]-self.disp_res_max[1])/2)
        self.full_screen = pygame.Surface(self.disp_res_max)
        self.framerate = 60
        self.clock = pygame.time.Clock()
        
        self.shared_dict = {}
        self.current_mode = False
        
        #test stuff
        self.current_mode = TestMode(self.SCREEN_SIZE, self.shared_dict)
        
    def __del__(self):
        """End and delete things as needed."""
        pygame.quit()
        
    def windowSet(self, scale_change):
        """Set the window to a scale of upscale + scale_change."""
        self.upscale += scale_change
        self.disp_res = (self.SCREEN_SIZE[0]*self.upscale, self.SCREEN_SIZE[1]*self.upscale)
        if not sys.platform.startswith('freebsd') and not sys.platform.startswith('darwin'):
            os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % ((self.monitor_res[0]-self.disp_res[0])//2, (self.monitor_res[1]-self.disp_res[1])//2)
        self.disp_screen = pygame.display.set_mode(self.disp_res)
        self.screen.convert()
        self.is_fullscreen = False
        
    def windowSetFullscreen(self):
        """Set the window to fullscreen."""
        self.disp_screen = pygame.display.set_mode(self.monitor_res, pygame.FULLSCREEN)
        self.full_screen.convert()
        self.screen.convert(self.full_screen)
        self.is_fullscreen = True
        
    def run(self):
        """Run the game, and check if the game needs to end."""
        if not self.running:
            #put something here maybe, could ask "are you sure you want to quit", etc
            if False:
                self.running = True
            else:
                return False
        self.event_list = self.filterInput()
        if self.current_mode:
            self.current_mode.input(self.event_list)
            self.current_mode.update()
            self.current_mode.draw(self.screen)
            if self.current_mode.done:
                #might need to check some values here
                #but probably not, b/c of shared_dict
                self.current_mode = False
        else:
            self.input(self.event_list)
            self.update()
            self.draw(self.screen)
        self.scaleThings()
        self.time()
        return True
        
    def stillNeedsHandling(self, event):
        """If event should be handled before all others, handle it and return False, otherwise return True.
        As an example, game-ending or display-changing events should be handled before all others.
        """
        if event.type == pygame.QUIT:
            self.running = False
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
                return False
            #Window re-sizing stuff
            elif event.key == pygame.K_PAGEUP or event.key == pygame.K_PERIOD:
                if self.upscale < self.upscale_max:
                    self.windowSet(1)
                return False
            elif event.key == pygame.K_PAGEDOWN or event.key == pygame.K_COMMA:
                if self.upscale > 1:
                    self.windowSet(-1)
                return False
            elif event.key == pygame.K_F11 or event.key == pygame.K_TAB:
                if self.is_fullscreen:
                    self.windowSet(0)
                else:
                    self.windowSetFullscreen()
                return False
        return True
        
    def filterInput(self):
        """Take care of input that game modes should not take care of."""
        return filter(self.stillNeedsHandling, pygame.event.get())
        
    def input(self, event_list):
        """Take inputs as needed."""
        pass
        
    def update(self):
        """Update things as needed."""
        pass
        
    def draw(self, screen):
        """Draw things as needed."""
        pass
        
    def scaleThings(self):
        """Scale screen onto display surface, then flip the display."""
        if not self.is_fullscreen:
            pygame.transform.scale(self.screen, self.disp_res, self.disp_screen)
        else:
            pygame.transform.scale(self.screen, self.disp_res_max, self.full_screen)
            self.disp_screen.blit(self.full_screen, self.fullscreen_offset)
        pygame.display.flip()
        
    def time(self):
        """Take care of time stuff."""
        pygame.display.set_caption(str(self.clock.get_fps()))
        self.clock.tick(self.framerate)
        