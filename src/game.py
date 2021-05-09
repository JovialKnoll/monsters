import configparser

import pygame

import constants
import shared
import mode


class Game(object):
    __slots__ = (
        '_max_framerate',
        '_clock',
        '_current_mode',
    )

    def __init__(self):
        self._max_framerate = shared.config.getint(constants.CONFIG_SECTION, constants.CONFIG_MAX_FRAMERATE)
        self._clock = pygame.time.Clock()
        self._current_mode = mode.ModeOpening0()

    def _saveConfig(self):
        current_config = configparser.ConfigParser()
        for section, settings in constants.CONFIG_DEFAULTS.items():
            current_config[section] = {}
            for key in settings.keys():
                current_config[section][key] = shared.config[section][key]
        with open(constants.CONFIG_FILE, 'w') as file:
            current_config.write(file, space_around_delimiters=False)

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
            if not isinstance(self._current_mode.next_mode, mode.ModeGameMenu):
                pygame.mixer.music.unpause()
                pygame.mixer.unpause()
            self._current_mode = self._current_mode.next_mode
        if not shared.game_running:
            self._saveConfig()
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
                shared.display.changeScale(1)
                return False
            elif event.key in (pygame.K_PAGEDOWN, pygame.K_COMMA):
                shared.display.changeScale(-1)
                return False
            elif event.key in (pygame.K_F11, pygame.K_TAB):
                shared.display.toggleFullscreen()
                return False
        return True

    def _handleQuit(self):
        # pass quit events forward to the mode.ModeGameMenu, but not to other events
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
