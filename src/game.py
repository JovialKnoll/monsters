import pygame

import shared
from modegamemenu import ModeGameMenu
from modeopening0 import ModeOpening0


class Game(object):
    __slots__ = (
        '_max_framerate',
        '_clock',
        '_current_mode',
    )

    def __init__(self, max_framerate):
        pygame.init()
        self._max_framerate = max_framerate
        self._clock = pygame.time.Clock()
        self._current_mode = ModeOpening0()

    def __del__(self):
        pygame.quit()

    def run(self):
        """Run the game, and check if the game needs to end."""
        if not self._current_mode:
            raise RuntimeError("error: no current mode")
        self._current_mode.input_events(
            self._filterInput(pygame.event.get())
        )
        self._current_mode.update(
            self._getTime()
        )
        self._current_mode.draw(shared.display.screen)
        shared.display.scaleDraw()
        if self._current_mode.next_mode is not None:
            if isinstance(self._current_mode, ModeGameMenu):
                pygame.mixer.music.unpause()
                pygame.mixer.unpause()
            else:
                pygame.mixer.stop()
            self._current_mode = self._current_mode.next_mode
        return shared.game_running

    def _filterInput(self, events):
        """Take care of input that game modes should not take care of."""
        return map(shared.display.scaleMouseInput, filter(self._stillNeedsHandling, events))

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
                if not shared.display.is_fullscreen:
                    shared.display.screenSet(1)
                return False
            elif event.key in (pygame.K_PAGEDOWN, pygame.K_COMMA):
                if not shared.display.is_fullscreen:
                    shared.display.screenSet(-1)
                return False
            elif event.key in (pygame.K_F11, pygame.K_TAB):
                if shared.display.is_fullscreen:
                    shared.display.screenSet(0)
                else:
                    shared.display.screenSetFullscreen()
                return False
        return True

    def _handleQuit(self):
        # pass quit events forward to the ModeGameMenu, but not to other events
        if isinstance(self._current_mode, ModeGameMenu):
            return True
        self._current_mode = ModeGameMenu(self._current_mode)
        pygame.mixer.music.pause()
        pygame.mixer.pause()
        return False

    def _getTime(self):
        # just for debugging purposes
        pygame.display.set_caption(str(self._clock.get_fps()))
        return self._clock.tick(self._max_framerate)
