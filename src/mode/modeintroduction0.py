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
            return "first text"
        elif self.convo_key == 1:
            return "second text"
        else:
            return "third text"

    def _textButton(self, index):
        if self.convo_key == 0:
            return "Okay"
        elif self.convo_key == 1:
            return "Yup"
        else:
            return "I Agree"

    def _goButton(self, index):
        if self.convo_key < 2:
            self.convo_key += 1
            self._renderText()
        else:
            shared.state.protag_mon = Monster()
            self._stopMixer()
            self.next_mode = ModeMonConvo0()
