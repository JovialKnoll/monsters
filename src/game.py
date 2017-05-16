import pygame, os, sys, cPickle
from constants import *
from monster import *
from fontwrap import *
from gamemode import *

from testmode import *
from convomode0 import *
class Game(object):
    class State(object):
        Normal, Menu, Save, Load = range(4)
    def __init__(self):
        """Start and create things as needed."""
        pygame.init()
        self.running = True
        self.state = Game.State.Normal
        self.old_screen = False
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

        GameMode.shared['protag_mon'] = Monster()

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

    def _resetCursorBlink(self):
        self.cursor_switch = True
        self.cursor_timer = 0

    def _clearSaveStuff(self):
        self.save_name = ''
        self.cursor_position = 0
        self._resetCursorBlink()

    def _saveGame(self):
        """Save the game."""
        objects = ['asd', (1,2,3), 123]
        if not os.path.exists(SAVE_DIRECTORY):
            os.makedirs(SAVE_DIRECTORY)
        with open(os.path.join(SAVE_DIRECTORY, self.save_name + '.sav'), 'wb') as file:
            cPickle.dump(objects, file, cPickle.HIGHEST_PROTOCOL)

    def _menuEvent(self, event):
        if self.state is Game.State.Normal:
            pass
        elif self.state is Game.State.Menu:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = Game.State.Normal
                elif event.key == pygame.K_F1:
                    self._clearSaveStuff()
                    self.state = Game.State.Save
                elif event.key == pygame.K_F2:
                    self._clearSaveStuff()
                    self.state = Game.State.Load
                elif event.key == pygame.K_F3:
                    self.running = False
        elif self.state is Game.State.Save:
            if event.type == pygame.QUIT:
                self.state = Game.State.Menu
            elif event.type == pygame.KEYDOWN:
                char = event.unicode
                length = len(self.save_name)
                if event.key == pygame.K_ESCAPE:
                    self.state = Game.State.Menu
                elif event.key == pygame.K_RETURN:#also call on a button press
                    if self.save_name:
                        self._saveGame()
                        self.state = Game.State.Menu
                elif event.key == pygame.K_LEFT:
                    self.cursor_position = max(self.cursor_position-1, 0)
                    self._resetCursorBlink()
                elif event.key == pygame.K_RIGHT:
                    self.cursor_position = min(self.cursor_position+1, length)
                    self._resetCursorBlink()
                elif event.key in (pygame.K_UP, pygame.K_HOME):
                    self.cursor_position = 0
                    self._resetCursorBlink()
                elif event.key in (pygame.K_DOWN, pygame.K_END):
                    self.cursor_position = length
                    self._resetCursorBlink()
                elif event.key == pygame.K_DELETE:
                    self.save_name = self.save_name[:self.cursor_position] + self.save_name[self.cursor_position+1:]
                    self._resetCursorBlink()
                elif event.key == pygame.K_BACKSPACE:
                    if self.cursor_position > 0:
                        self.save_name = self.save_name[:self.cursor_position-1] + self.save_name[self.cursor_position:]
                        self.cursor_position -= 1
                    self._resetCursorBlink()
                elif length < 16 and ((char >= '0' and char <= '9' ) or (event.key > 96 and event.key < 123)):#numbers and letters
                    self.save_name = self.save_name[:self.cursor_position] + char + self.save_name[self.cursor_position:]
                    self.cursor_position += 1
                    self._resetCursorBlink()
        elif self.state is Game.State.Load:
            if event.type == pygame.QUIT:
                self.state = Game.State.Menu
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = Game.State.Menu
                #put in scrolling to select save file? maybe typing too? alphebatized list...
        else:
            raise NotImplementedError("self.state = " + str(self.state))

    def _menuInput(self, event_list):
        for event in event_list:
            self._menuEvent(event)

    def _menuUpdate(self):
        if self.state is Game.State.Normal:
            pass
        elif self.state is Game.State.Menu:
            pass
        elif self.state is Game.State.Save:
            if self.cursor_timer >= CURSOR_TIME:
                self.cursor_switch = not self.cursor_switch
                self.cursor_timer = 0
            self.cursor_timer += 1
        elif self.state is Game.State.Load:
            pass
        else:
            raise NotImplementedError("self.state = " + str(self.state))

    def _menuDraw(self, screen):
        if not self.old_screen:
            self.old_screen = screen.copy()
        screen.blit(self.old_screen, (0,0))
        if self.state is Game.State.Normal:
            pass
        elif self.state is Game.State.Menu:
            disp_text = "Options:\n_Go Back (ESC)\n_Save (F1)\n_Load (F2)\n_Quit (F3)"
            GameMode.shared['font_wrap'].renderToInside(screen, (0,0), 20 * FONT_SIZE, disp_text, False, WHITE, BLACK)
            #center this, make bigger and buttons... maybe
            #more to come
        elif self.state is Game.State.Save:
            disp_text = "Options:\n_Go Back (ESC)\n_Save (ENTER)\nType a file name:\n"
            if self.save_name:
                disp_text += self.save_name
            disp_text += ".sav"
            GameMode.shared['font_wrap'].renderToInside(screen, (0,0), 20 * FONT_SIZE, disp_text, False, WHITE, BLACK)
            if self.cursor_switch:
                screen.fill(WHITE, ((self.cursor_position * FONT_SIZE, 40), (1, 10)))
            #display prompt for file to save
            #display save_name in there
        elif self.state is Game.State.Load:
            disp_text = "Options:\n_Go Back (ESC)\n_Load (ENTER)\nSelect a file name:\n"
            disp_text += ".sav"
            GameMode.shared['font_wrap'].renderToInside(screen, (0,0), 20 * FONT_SIZE, disp_text, False, WHITE, BLACK)
            #draw load thingy
            pass
        else:
            raise NotImplementedError("self.state = " + str(self.state))

    def run(self):
        """Run the game, and check if the game needs to end."""
        if not self.running:
            return False
        event_list = self._filterInput(pygame.event.get())
        if self.state is not Game.State.Normal:
            self._menuInput(event_list)
            self._menuUpdate()
            self._menuDraw(self.screen)
        elif self.current_mode:
            self.current_mode.input(event_list)
            self.current_mode.update()
            self.current_mode.draw(self.screen)
            if self.current_mode.next_mode != False:
                self.current_mode = self.current_mode.next_mode
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
        if self.state is Game.State.Normal:
            self.old_screen = False
            self.state = Game.State.Menu
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
