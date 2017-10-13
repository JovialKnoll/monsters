from convomode import *

class MonConvoMode(ConvoMode):
    def __init__(self):
        super(MonConvoMode, self).__init__()
        self.shared.protag_mon.drawCentered(self.background, (160,128))
