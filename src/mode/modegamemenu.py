import pygame

import constants
import shared
from save import Save

from .mode import Mode


class ModeGameMenu(Mode):
    MENU_WIDTH = 20
    FILE_EXT = '.sav'
    SHARED_DISP_TEXT = "Options:\n_Go Back (ESC)\n"

    __slots__ = (
        '_previous_mode',
        '_old_screen',
    )

    def __init__(self, previous_mode):
        super().__init__()
        self._previous_mode = previous_mode
        self._old_screen = pygame.Surface(constants.SCREEN_SIZE).convert(shared.display.screen)
        self._previous_mode.draw(self._old_screen)

    def _drawScreen(self, screen):
        screen.blit(self._old_screen, (0, 0))

    @classmethod
    def _drawText(cls, screen, disp_text):
        shared.font_wrap.renderToInside(
            screen,
            (0, 0),
            cls.MENU_WIDTH * constants.FONT_SIZE,
            disp_text,
            False,
            constants.WHITE,
            constants.BLACK
        )


class ModeGameMenuTop(ModeGameMenu):
    def _input(self, event):
        if event.type == pygame.QUIT:
            shared.game_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next_mode = self._previous_mode
            elif event.key == pygame.K_F1:
                self.next_mode = ModeGameMenuSave(self._previous_mode)
            elif event.key == pygame.K_F2:
                self.next_mode = ModeGameMenuLoad(self._previous_mode)
            elif event.key == pygame.K_F3:
                shared.game_running = False

    def _drawScreen(self, screen):

        super()._drawScreen(screen)
        disp_text = self.SHARED_DISP_TEXT
        disp_text += "_Save (F1)\n_Load (F2)\n_Quit (F3)"
        self._drawText(screen, disp_text)


class ModeGameMenuSave(ModeGameMenu):
    __slots__ = (
        '_save_name',
        '_cursor_position',
        '_confirm_overwrite',
        '_save_success',
        '_cursor_switch',
        '_cursor_timer',
    )

    def __init__(self, previous_mode):
        super().__init__(previous_mode)
        self._save_name = ''
        self._resetCursorBlink()
        self._cursor_position = 0
        self._confirm_overwrite = False
        self._save_success = None

    def _resetCursorBlink(self):
        self._cursor_switch = True
        self._cursor_timer = 0

    def _input(self, event):
        if event.type == pygame.QUIT:
            self.next_mode = ModeGameMenuTop(self._previous_mode)
        elif event.type == pygame.KEYDOWN:
            char = event.unicode
            length = len(self._save_name)
            if self._save_success:
                self.next_mode = ModeGameMenuTop(self._previous_mode)
            elif event.key == pygame.K_ESCAPE:
                if self._confirm_overwrite:
                    self._confirm_overwrite = False
                    self._save_success = None
                else:
                    self.next_mode = ModeGameMenuTop(self._previous_mode)
            elif event.key == pygame.K_RETURN:
                if self._save_name and self._previous_mode.canSave():
                    if Save.willOverwrite(self._save_name + self.FILE_EXT) and not self._confirm_overwrite:
                        self._confirm_overwrite = True
                    elif not self._save_success:
                        new_save = Save.getFromMode(self._save_name + self.FILE_EXT, self._previous_mode)
                        self._save_success = new_save.save()
            elif event.key == pygame.K_LEFT:
                self._cursor_position = max(self._cursor_position - 1, 0)
                self._resetCursorBlink()
            elif event.key == pygame.K_RIGHT:
                self._cursor_position = min(self._cursor_position + 1, length)
                self._resetCursorBlink()
            elif event.key in (pygame.K_UP, pygame.K_HOME):
                self._cursor_position = 0
                self._resetCursorBlink()
            elif event.key in (pygame.K_DOWN, pygame.K_END):
                self._cursor_position = length
                self._resetCursorBlink()
            elif event.key == pygame.K_DELETE:
                self._save_name = self._save_name[:self._cursor_position] + self._save_name[self._cursor_position + 1:]
                self._resetCursorBlink()
            elif event.key == pygame.K_BACKSPACE:
                if self._cursor_position > 0:
                    self._save_name = self._save_name[:self._cursor_position - 1] \
                        + self._save_name[self._cursor_position:]
                    self._cursor_position -= 1
                self._resetCursorBlink()
            elif (
                length < (self.MENU_WIDTH - len(self.FILE_EXT) - 1)
                and (
                    # numbers
                    ('0' <= char <= '9')
                    # or letters
                    or (96 < event.key < 123)
                )
            ):
                self._save_name = self._save_name[:self._cursor_position] \
                    + char \
                    + self._save_name[self._cursor_position:]
                self._cursor_position += 1
                self._resetCursorBlink()

    def update(self, dt):
        self._cursor_timer += dt
        if self._cursor_timer >= constants.CURSOR_TIME:
            self._cursor_switch = not self._cursor_switch
            self._cursor_timer -= constants.CURSOR_TIME

    def _drawScreen(self, screen):
        super()._drawScreen(screen)
        disp_text = self.SHARED_DISP_TEXT
        if not self._previous_mode.canSave():
            disp_text += "\nYou can't save now."
        elif not self._save_success:
            disp_text += "_Save (ENTER)\nType a file name:\n>"
            if self._save_name:
                disp_text += self._save_name
            disp_text += self.FILE_EXT
            if self._confirm_overwrite and self._save_success is None:
                disp_text += "\nThis will overwrite an existing save file." \
                    + "\nPress ENTER again to confirm, or ESC to go back."
            elif self._save_success is False:
                disp_text += "\nSave failed.\nPress ENTER to try again, or ESC to go back."
        else:
            disp_text += "\nSaved successfully.\nPress any key to go back."
        self._drawText(screen, disp_text)
        if self._cursor_switch and not self._confirm_overwrite and self._save_success is None:
            screen.fill(
                constants.WHITE,
                (
                    ((self._cursor_position + 1) * constants.FONT_SIZE, 4 * constants.FONT_HEIGHT),
                    (1, constants.FONT_HEIGHT)
                )
            )


class ModeGameMenuLoad(ModeGameMenu):
    __slots__ = (
        '_saves',
        '_save_index',
        '_loaded_save',
    )

    def __init__(self, previous_mode):
        super().__init__(previous_mode)
        self._saves = Save.getAllFromFiles()
        self._save_index = 0
        self._loaded_save = False

    def _input(self, event):
        if event.type == pygame.QUIT:
            self.next_mode = ModeGameMenuTop(self._previous_mode)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or self._loaded_save:
                self.next_mode = ModeGameMenuTop(self._previous_mode)
            elif len(self._saves) > 0:
                if event.key in (pygame.K_UP, pygame.K_LEFT):
                    self._save_index = max(self._save_index - 1, 0)
                    pass
                elif event.key in (pygame.K_DOWN, pygame.K_RIGHT):
                    self._save_index = min(self._save_index + 1, len(self._saves) - 1)
                    pass
                elif event.key == pygame.K_RETURN:
                    self._previous_mode = self._saves[self._save_index].load()
                    self._previous_mode.draw(self._old_screen)
                    self._loaded_save = True
                    pass

    def _drawScreen(self, screen):
        super()._drawScreen(screen)
        disp_text = self.SHARED_DISP_TEXT
        if len(self._saves) == 0:
            disp_text += "\nThere are no save files to select from."
        elif self._loaded_save:
            disp_text += "\nLoaded successfully.\nPress any key to go back."
        else:
            disp_text += "_Load (ENTER)\nSelect a file (ARROW KEYS):"
            for i in range(-1, 2):
                disp_text += "\n"
                this_index = self._save_index + i
                if i == 0:
                    disp_text += ">"
                else:
                    disp_text += "_"
                if 0 <= this_index < len(self._saves):
                    disp_text += self._saves[this_index].file_name
        self._drawText(screen, disp_text)
