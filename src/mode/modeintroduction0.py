import shared
from monster import Monster

from .modeconvo import ModeConvo
from .modemonconvo0 import ModeMonConvo0


class ModeIntroduction0(ModeConvo):
    __slots__ = (
    )

    def __init__(self):
        super().__init__(0)

    def _textMain(self):
        if self.convo_key == 0:
            return "Okay so first off thank you so much for volunteering!" \
                   + "\n\nWe're always trying to get more participants for the human-monster mentorship program" \
                   + " so it really means a lot."
        elif self.convo_key == 1:
            return "Now I know some of you have been here before," \
                   + " but I can see at least a few new faces among us." \
                   + "\n\nSo, I'll go ahead and give the program overview before we get started."
        else:
            return "third text"

    def _textButton(self, index):
        return "continue"

    def _goButton(self, index):
        if self.convo_key < 2:
            self.convo_key += 1
            self._renderText()
        else:
            shared.state.protag_mon = Monster()
            self._stopMixer()
            self.next_mode = ModeMonConvo0()
