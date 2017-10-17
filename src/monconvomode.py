import state

from convomode import ConvoMode

class MonConvoMode(ConvoMode):
    def _drawScreen(self, screen):
        super(MonConvoMode, self)._drawScreen(screen)
        state.state.protag_mon.drawCentered(screen, (160,128))
