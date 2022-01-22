import typing

import pygame

import constants
import shared
import mode


class Game(object):
    __slots__ = (
        '_max_framerate',
        '_clock',
        '_current_mode',
        '_is_first_loop',
    )

    def __init__(self):
        self._max_framerate = shared.config.getint(constants.CONFIG_SECTION, constants.CONFIG_MAX_FRAMERATE)
        self._clock = pygame.time.Clock()
        self._current_mode = mode.ModeOpening0()
        self._is_first_loop = True

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
            if isinstance(self._current_mode, mode.ModeGameMenu) \
                    and not isinstance(self._current_mode.next_mode, mode.ModeGameMenu):
                pygame.mixer.music.unpause()
                pygame.mixer.unpause()
            self._current_mode.all_sprites.empty()
            self._current_mode = self._current_mode.next_mode
        if not shared.game_running:
            shared.saveConfig()
        self._is_first_loop = False
        return shared.game_running

    def _filterInput(self, events: typing.Iterable[pygame.event.Event]):
        """Take care of input that game modes should not take care of."""
        return filter(self._stillNeedsHandling, map(shared.display.scaleMouseInput, events))

    def _stillNeedsHandling(self, event: pygame.event.Event):
        """If event should be handled before all others, handle it and return False, otherwise return True.
        As an example, game-ending or display-changing events should be handled before all others.
        Also filter out bad mouse events here.
        """
        if event.type in (pygame.QUIT, pygame.WINDOWFOCUSLOST, pygame.WINDOWMINIMIZED):
            return self._handlePauseMenu()
        elif event.type == pygame.WINDOWMOVED and not self._is_first_loop:
            return self._handlePauseMenu()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return self._handlePauseMenu()
        elif event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN) \
            and (
                event.pos[0] < 0
                or event.pos[1] < 0
                or event.pos[0] >= constants.SCREEN_SIZE[0]
                or event.pos[1] >= constants.SCREEN_SIZE[1]
        ):
            return False
        return True

    def _handlePauseMenu(self):
        # pass quit events forward to mode.ModeGameMenu, but not to other modes
        if isinstance(self._current_mode, mode.ModeGameMenu):
            return True
        self._current_mode = mode.ModeGameMenuTop(self._current_mode)
        pygame.mixer.music.pause()
        pygame.mixer.pause()
        return False

    def _getTime(self):
        # just for debugging purposes
        pygame.display.set_caption(str(self._clock.get_fps()))
        return self._clock.tick(self._max_framerate)
