import state

from convomode import *

class MonConvoMode(ConvoMode):
    def _drawScreen(self, screen):
        super(MonConvoMode, self)._drawScreen(screen)
        state.state.protag_mon.drawCentered(screen, (160,128))
