import os
import pickle

import pygame

import constants
import shared
from mode import Mode


class ModeGameMenu(Mode):
    class State(object):
        Menu, Save, Load = range(3)
    menu_width = 20
    file_extension = '.sav'

    __slots__ = (
        '_state',
        '_previous_mode',
        '_old_screen',
        '_cursor_switch',
        '_cursor_timer',
        '_save_name',
        '_cursor_position',
    )

    def __init__(self, previous_mode):
        super().__init__()
        self._state = ModeGameMenu.State.Menu
        self._previous_mode = previous_mode
        self._old_screen = pygame.Surface(constants.SCREEN_SIZE).convert(shared.display.screen)
        previous_mode.draw(self._old_screen)
        self._clearSaveStuff()

    def _resetCursorBlink(self):
        self._cursor_switch = True
        self._cursor_timer = 0

    def _clearSaveStuff(self):
        self._save_name = ''
        self._cursor_position = 0
        self._resetCursorBlink()

    def _saveGame(self):
        """Save the game."""
        # check if current mode implements save?
        objects = ['asd', (1, 2, 3), 123]
        if not os.path.exists(constants.SAVE_DIRECTORY):
            os.makedirs(constants.SAVE_DIRECTORY)
        with open(
            os.path.join(
                constants.SAVE_DIRECTORY,
                self._save_name + self.__class__.file_extension
            ),
            'wb'
        ) as f:
            pickle.dump(objects, f, pickle.HIGHEST_PROTOCOL)

    def _inputMenu(self, event):
        if event.type == pygame.QUIT:
            shared.game_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next_mode = self._previous_mode
            elif event.key == pygame.K_F1:
                self._clearSaveStuff()
                self._state = ModeGameMenu.State.Save
            elif event.key == pygame.K_F2:
                self._clearSaveStuff()
                self._state = ModeGameMenu.State.Load
            elif event.key == pygame.K_F3:
                shared.game_running = False

    def _inputSave(self, event):
        if event.type == pygame.QUIT:
            self._state = ModeGameMenu.State.Menu
        elif event.type == pygame.KEYDOWN:
            char = event.unicode
            length = len(self._save_name)
            if event.key == pygame.K_ESCAPE:
                self._state = ModeGameMenu.State.Menu
            elif event.key == pygame.K_RETURN:
                # also call on a button press
                if self._save_name:
                    self._saveGame()
                    self._state = ModeGameMenu.State.Menu
            elif event.key == pygame.K_LEFT:
                self._cursor_position = max(self._cursor_position - 1, 0)
                self._resetCursorBlink()
            elif event.key == pygame.K_RIGHT:
                self._cursor_position = min(self._cursor_position+1, length)
                self._resetCursorBlink()
            elif event.key in (pygame.K_UP, pygame.K_HOME):
                self._cursor_position = 0
                self._resetCursorBlink()
            elif event.key in (pygame.K_DOWN, pygame.K_END):
                self._cursor_position = length
                self._resetCursorBlink()
            elif event.key == pygame.K_DELETE:
                self._save_name = self._save_name[:self._cursor_position] + self._save_name[self._cursor_position+1:]
                self._resetCursorBlink()
            elif event.key == pygame.K_BACKSPACE:
                if self._cursor_position > 0:
                    self._save_name = self._save_name[:self._cursor_position-1] \
                        + self._save_name[self._cursor_position:]
                    self._cursor_position -= 1
                self._resetCursorBlink()
            elif (
                length < (self.__class__.menu_width - len(self.__class__.file_extension))
                and (
                    # numbers
                    ('0' <= char <= '9')
                    # or letters
                    or (96 < event.key < 123)
                )
            ):
                self._save_name = self._save_name[:self._cursor_position]\
                    + char\
                    + self._save_name[self._cursor_position:]
                self._cursor_position += 1
                self._resetCursorBlink()

    def _inputLoad(self, event):
        if event.type == pygame.QUIT:
            self._state = ModeGameMenu.State.Menu
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._state = ModeGameMenu.State.Menu
            # put in scrolling to select save file? maybe typing too? alphabetized list...

    def _input(self, event):
        if self._state is ModeGameMenu.State.Menu:
            self._inputMenu(event)
        elif self._state is ModeGameMenu.State.Save:
            self._inputSave(event)
        elif self._state is ModeGameMenu.State.Load:
            self._inputLoad(event)
        else:
            raise RuntimeError("error: self._state = " + str(self._state))

    def update(self, dt):
        if self._state is ModeGameMenu.State.Menu:
            pass
        elif self._state is ModeGameMenu.State.Save:
            self._cursor_timer += dt
            if self._cursor_timer >= constants.CURSOR_TIME:
                self._cursor_switch = not self._cursor_switch
                self._cursor_timer -= constants.CURSOR_TIME
        elif self._state is ModeGameMenu.State.Load:
            pass
        else:
            raise RuntimeError("error: self._state = " + str(self._state))

    def _drawScreen(self, screen):
        screen.blit(self._old_screen, (0, 0))
        if self._state is ModeGameMenu.State.Menu:
            disp_text = "Options:\n_Go Back (ESC)\n_Save (F1)\n_Load (F2)\n_Quit (F3)"
            shared.font_wrap.renderToInside(
                screen,
                (0, 0),
                self.__class__.menu_width * constants.FONT_SIZE,
                disp_text,
                False,
                constants.WHITE,
                constants.BLACK
            )
            # center this, make bigger and buttons... maybe
            # more to come
        elif self._state is ModeGameMenu.State.Save:
            disp_text = "Options:\n_Go Back (ESC)\n_Save (ENTER)\nType a file name:\n"
            if self._save_name:
                disp_text += self._save_name
            disp_text += self.__class__.file_extension
            shared.font_wrap.renderToInside(
                screen,
                (0, 0),
                self.__class__.menu_width * constants.FONT_SIZE,
                disp_text,
                False,
                constants.WHITE,
                constants.BLACK
            )
            if self._cursor_switch:
                screen.fill(
                    constants.WHITE,
                    (
                        (self._cursor_position * constants.FONT_SIZE, 4 * constants.FONT_HEIGHT),
                        (1, constants.FONT_HEIGHT)
                    )
                )
            # display prompt for file to save
            # display save_name in there
        elif self._state is ModeGameMenu.State.Load:
            disp_text = "Options:\n_Go Back (ESC)\n_Load (ENTER)\nSelect a file name:\n"
            disp_text += self.__class__.file_extension
            shared.font_wrap.renderToInside(
                screen,
                (0, 0),
                self.__class__.menu_width * constants.FONT_SIZE,
                disp_text,
                False,
                constants.WHITE,
                constants.BLACK
            )
            # draw load thingy
            pass
        else:
            raise RuntimeError("error: self._state = " + str(self._state))
