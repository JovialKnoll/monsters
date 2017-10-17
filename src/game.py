import pygame

import constants
import shared
from gamemenumode import GameMenuMode
#from testmode import TestMode
from convomode0 import ConvoMode0

class Game(object):
    def __init__(self):
        """Start and create things as needed."""
        pygame.init()
        # time
        self.clock = pygame.time.Clock()
        # mode (must be set before running
        self.current_mode = None
        # test stuff
        # self.current_mode = TestMode()
        self.current_mode = ConvoMode0()

    def __del__(self):
        """End and delete things as needed."""
        pygame.quit()

    def run(self):
        """Run the game, and check if the game needs to end."""
        if not self.current_mode:
            raise RuntimeError("error: no current mode")
        self.current_mode.input_events(
            self._filterInput(pygame.event.get())
        )
        self._getTime()
        # todo(?): pass result to .update()
        self.current_mode.update()
        self.current_mode.draw()
        self._scaleDraw()
        if self.current_mode.next_mode is not None:
            self.current_mode = self.current_mode.next_mode
        return shared.game_running

    def _filterInput(self, events):
        """Take care of input that game modes should not take care of."""
        return map(self._scaleMouseInput, filter(self._stillNeedsHandling, events))

    def _stillNeedsHandling(self, event):
        """If event should be handled before all others, handle it and return False, otherwise return True.
        As an example, game-ending or display-changing events should be handled before all others.
        """
        if event.type == pygame.QUIT:
            return self._handleQuit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return self._handleQuit()
            # window re-sizing stuff
            elif event.key in (pygame.K_PAGEUP, pygame.K_PERIOD):
                if not shared.is_fullscreen:
                    shared.screenSet(1)
                return False
            elif event.key in (pygame.K_PAGEDOWN, pygame.K_COMMA):
                if not shared.is_fullscreen:
                    shared.screenSet(-1)
                return False
            elif event.key in (pygame.K_F11, pygame.K_TAB):
                if shared.is_fullscreen:
                    shared.screenSet(0)
                else:
                    shared.screenSetFullscreen()
                return False
        return True

    def _handleQuit(self):
        # pass quit events forward to the GameMenuMode, but not to other events
        if isinstance(self.current_mode, GameMenuMode):
            return True
        self.current_mode = GameMenuMode(self.current_mode)
        return False

    def _scaleMouseInput(self, event):
        """Scale mouse position for events in terms of the screen (as opposed to the display surface)."""
        if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):
            if shared.is_fullscreen:
                event_dict = {
                    'pos': (
                        (event.pos[0] - shared.fullscreen_offset[0]) // shared.upscale_max,
                        (event.pos[1] - shared.fullscreen_offset[1]) // shared.upscale_max,
                    )
                }
            else:
                event_dict = {
                    'pos': (
                        event.pos[0] // shared.upscale,
                        event.pos[1] // shared.upscale,
                    )
                }
            if event.type == pygame.MOUSEMOTION:
                event_dict['rel'] = event.rel
                event_dict['buttons'] = event.buttons
            else:
                event_dict['button'] = event.button
            return pygame.event.Event(event.type, event_dict)
        return event

    def _getTime(self):
        """Take care of time stuff."""
        pygame.display.set_caption(str(self.clock.get_fps()))# just for debugging purposes
        return self.clock.tick(constants.MAX_FRAMERATE)

    def _scaleDraw(self):
        """Scale screen onto display surface, then flip the display."""
        if not shared.is_fullscreen:
            pygame.transform.scale(shared.screen, shared.disp_res, shared.disp_screen)
        else:
            pygame.transform.scale(shared.screen, shared.disp_res_max, shared.full_screen)
            shared.disp_screen.blit(shared.full_screen, shared.fullscreen_offset)
        pygame.display.flip()
