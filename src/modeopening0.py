import pygame

import constants
import shared
from mode import Mode
from modeopening1 import ModeOpening1
from animsprite import AnimSprite

class ModeOpening0(Mode):
    __slots__ = (
        'time',
        'step',
        'background',
    )

    logo_text = "Jovial Knoll"

    def __init__(self):
        super(ModeOpening0, self).__init__()

        self.time = 0
        self.step = 0
        self.background = pygame.Surface(constants.SCREEN_SIZE).convert(shared.display.screen)
        self.background.fill(constants.WHITE)
        shared.font_wrap.renderToCentered(
            self.background,
            (constants.SCREEN_SIZE[0] // 2, constants.SCREEN_SIZE[1] * 5 // 8),
            self.__class__.logo_text,
            False,
            constants.BLACK
        )
        jk_logo = pygame.image.load(constants.JK_LOGO_BLACK).convert(shared.display.screen)
        self.background.blit(
            jk_logo,
            (
                constants.SCREEN_SIZE[0] // 2 - jk_logo.get_width() // 2,
                constants.SCREEN_SIZE[1] * 7 // 16 - jk_logo.get_height() // 2,
            )
        )
        star_sprite = AnimSprite()
        star_sprite.image = pygame.image.load(constants.STAR).convert(shared.display.screen)
        star_sprite.image.set_colorkey(constants.COLORKEY)
        star_sprite.rect = star_sprite.image.get_rect()
        star_sprite.rect.center = (
            constants.SCREEN_SIZE[0] // 2 + constants.SCREEN_SIZE[1] // 2 + star_sprite.rect.width // 2,
            star_sprite.rect.height // 2 * -1,
        )
        star_sprite.addWait(750)
        star_sprite.addPosAbs(
            AnimSprite.Lerp,
            500,
            constants.SCREEN_SIZE[0] // 2 - constants.SCREEN_SIZE[1] // 2 - star_sprite.rect.width // 2,
            constants.SCREEN_SIZE[1] + star_sprite.rect.height // 2
        )
        self.all_sprites.add(star_sprite)

    def _changeMode(self):
        self.next_mode = ModeOpening1()

    def _input(self, event):
        if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
            self._changeMode()

    def _update(self, dt):
        self.time += dt
        if self.time >= 1250 and self.step < 1:
            self.step += 1
            shared.font_wrap.renderToCentered(
                self.background,
                (constants.SCREEN_SIZE[0] // 2, constants.SCREEN_SIZE[1] * 5 // 8),
                self.__class__.logo_text,
                False,
                constants.TEXT_COLOR
            )
        if self.time >= 1500 and self.step < 2:
            self.step += 1
            shared.font_wrap.renderToCentered(
                self.background,
                (constants.SCREEN_SIZE[0] // 2, constants.SCREEN_SIZE[1] * 5 // 8),
                self.__class__.logo_text,
                False,
                constants.DARK_TEXT_COLOR
            )
            jk_logo = pygame.image.load(constants.JK_LOGO_LIGHT_GREY).convert(shared.display.screen)
            self.background.blit(
                jk_logo,
                (
                    constants.SCREEN_SIZE[0] // 2 - jk_logo.get_width() // 2,
                    constants.SCREEN_SIZE[1] * 7 // 16 - jk_logo.get_height() // 2,
                )
            )
        if self.time >= 1750 and self.step < 3:
            self.step += 1
            shared.font_wrap.renderToCentered(
                self.background,
                (constants.SCREEN_SIZE[0] // 2, constants.SCREEN_SIZE[1] * 5 // 8),
                self.__class__.logo_text,
                False,
                constants.BLACK
            )
            jk_logo = pygame.image.load(constants.JK_LOGO_GREY).convert(shared.display.screen)
            self.background.blit(
                jk_logo,
                (
                    constants.SCREEN_SIZE[0] // 2 - jk_logo.get_width() // 2,
                    constants.SCREEN_SIZE[1] * 7 // 16 - jk_logo.get_height() // 2,
                )
            )
        if self.time >= 4250 and self.step < 4:
            self._changeMode()
            pass

    def _drawScreen(self, screen):
        screen.blit(self.background, (0, 0))
