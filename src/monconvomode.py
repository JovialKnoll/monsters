import shared
from convomode import ConvoMode

class MonConvoMode(ConvoMode):
    __slots__ = (
    )

    def _drawScreen(self, screen):
        super(MonConvoMode, self)._drawScreen(screen)
        shared.state.protag_mon.drawCentered(screen, (160,128))
