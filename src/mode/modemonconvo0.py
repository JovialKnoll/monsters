import shared
from monster import Monster

from .modeconvo import ModeConvo
from .modetest import ModeTest
from .modefight import ModeFight


class ModeMonConvo0(ModeConvo):
    def _handleButton(self, prev_convo_key: str, index: int):
        if index == 1:
            print("Really anything can happen here.")
            self._stopMixer()
            self.next_mode = ModeFight(
                shared.state.protag_mon,
                Monster.atLevel(0),
                ModeMonConvo0,
                ModeMonConvo0,
                ModeTest
            )
            return True
        elif index == 3:
            print("The other main thing would be to have pressing a button change the mode.\n"
                  + "It could set variables and then change the mode.")
        return False
