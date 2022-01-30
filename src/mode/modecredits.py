import constants
import shared
from animsprite import AnimSprite
from .modeopening0 import ModeOpening0
from .modeopening import ModeOpening


class ModeCredits(ModeOpening):
    __slots__ = (
        '_time',
    )

    def __init__(self):
        super().__init__()
        self._time = 0
        # could replace time tracking with tracking position of sprite
        with open(constants.CREDITS_TEXT) as credits_file:
            credits_text = credits_file.read().replace(' ', '_')
        credits_sprite = AnimSprite()
        credits_sprite.image = shared.font_wrap.renderInside(
            constants.SCREEN_SIZE[0] // 2,
            credits_text,
            False,
            constants.WHITE,
            background=constants.BLACK
        )
        credits_sprite.rect = credits_sprite.image.get_rect()
        credits_sprite.rect.midtop = (
            constants.SCREEN_SIZE[0] // 2,
            constants.SCREEN_SIZE[1],
        )
        credits_sprite.addWait(1000)
        credits_sprite.addPosRel(
            AnimSprite.Lerp,
            10000,
            0,
            (constants.SCREEN_SIZE[1] + credits_sprite.rect.height) * -1
        )
        self.all_sprites.add(credits_sprite)

    def _switchMode(self):
        self.next_mode = ModeOpening0()

    def _update(self, dt):
        self._time += dt
        # after enough time for the credits to scroll, render text on to background
        # press any key to proceed etc

    def _drawScreen(self, screen):
        screen.fill(constants.BLACK)
