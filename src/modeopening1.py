import math

import pygame

import constants
import shared
from mode import Mode
from modeopening2 import ModeOpening2
from animsprite import AnimSprite


class ModeOpening1(Mode):
    LOGO_TEXT = "tinsil"
    STAR_WAVES = 3
    STAR_WAIT = 1000
    STAR_TRAVEL = 350

    __slots__ = (
        'time',
        'background',
        'logo',
    )

    def __init__(self):
        super().__init__()

        self.time = 0
        self.background = pygame.Surface(constants.SCREEN_SIZE).convert(shared.display.screen)
        self.background.fill(constants.WHITE)
        shared.font_wrap.renderToCentered(
            self.background,
            (constants.SCREEN_SIZE[0] // 2, constants.SCREEN_SIZE[1] * 5 // 8 + 8),
            self.__class__.LOGO_TEXT,
            False,
            constants.BLACK
        )
        bip = pygame.mixer.Sound(constants.BIP)
        self.logo = pygame.image.load(constants.TIN_LOGO).convert(shared.display.screen)
        self.logo.set_colorkey(constants.COLORKEY)
        star_image = pygame.image.load(constants.STAR).convert(shared.display.screen)
        star_image.set_colorkey(constants.COLORKEY)
        star_image = pygame.transform.scale(
            star_image,
            (
                star_image.get_width() // 2,
                star_image.get_height() // 2,
            )
        )
        star_number = 7
        for i in range(self.__class__.STAR_WAVES):
            for j in range(star_number):
                radius = constants.SCREEN_SIZE[0] * 5 // 8
                angle = j * 2 / star_number * math.pi
                x = constants.SCREEN_SIZE[0] // 2 + radius * math.sin(angle)
                y = constants.SCREEN_SIZE[1] // 2 - radius * math.cos(angle)
                self.makeStar(
                    star_image,
                    self.__class__.STAR_WAIT + i * self.__class__.STAR_TRAVEL,
                    (x, y),
                    bip if j == 0 else None
                )

    def makeStar(self, image, wait, dest, sound):
        star_sprite = AnimSprite()
        star_sprite.image = image
        star_sprite.rect = star_sprite.image.get_rect()
        star_sprite.rect.center = (
            constants.SCREEN_SIZE[0] // 2,
            constants.SCREEN_SIZE[1] // 2,
        )
        star_sprite.addWait(wait, sound=sound)
        star_sprite.addPosAbs(
            AnimSprite.Lerp,
            self.__class__.STAR_TRAVEL,
            dest
        )
        self.all_sprites.add(star_sprite)

    def _changeMode(self):
        self.next_mode = ModeOpening2()

    def _input(self, event):
        if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
            self._changeMode()

    def _update(self, dt):
        self.time += dt
        if self.time >= self.__class__.STAR_WAIT * 2 + self.__class__.STAR_TRAVEL * self.__class__.STAR_WAVES:
            self._changeMode()

    def _drawScreen(self, screen):
        screen.blit(self.background, (0, 0))

    def _drawPostSprites(self, screen):
        screen.blit(
            self.logo,
            (
                constants.SCREEN_SIZE[0] // 2 - self.logo.get_width() // 2,
                constants.SCREEN_SIZE[1] * 7 // 16 - self.logo.get_height() // 2,
            )
        )
