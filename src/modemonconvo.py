import shared
from modeconvo import ModeConvo

class ModeMonConvo(ModeConvo):
    __slots__ = (
    )

    def _drawScreen(self, screen):
        super(ModeMonConvo, self)._drawScreen(screen)
        shared.state.protag_mon.drawCentered(screen, (160,128))
