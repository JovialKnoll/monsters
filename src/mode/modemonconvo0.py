import shared
from monster import Monster

from .modemonconvo import ModeMonConvo
from .modetest import ModeTest
from .modefight import ModeFight
from .modemenu import ModeMenu


class ModeMonConvo0(ModeMonConvo):
    __slots__ = (
    )

    def _handleButton(self, prev_convo_key: str, index: int):
        if index == 0:
            print("Button 0 was pressed.")
            self._stopMixer()
            self.next_mode = ModeTest()
        elif index == 1:
            print("Really anything can happen here.")
            self._stopMixer()
            self.next_mode = ModeFight(
                shared.state.protag_mon,
                Monster.atLevel(0),
                ModeMonConvo0,
                ModeMonConvo0,
                ModeTest
            )
        elif index == 2:
            print("The main thing would be to have pressing a button set variables.")
            self._stopMixer()
            self.next_mode = ModeMenu()
        elif index == 3:
            print("The other main thing would be to have pressing a button change the mode.\n"
                  + "It could set variables and then change the mode.")
