import shared
from convomode import ConvoMode

class MonConvoMode(ConvoMode):
    def _drawScreen(self, screen):
        super(MonConvoMode, self)._drawScreen(screen)
        shared.state.protag_mon.drawCentered(screen, (160,128))
