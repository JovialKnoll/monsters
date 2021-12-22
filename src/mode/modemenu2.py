import shared
from monster import Monster
from personality import Personality
from .modefight import ModeFight
from .modetalkwin2 import ModeTalkWin2
from .modetalkelse2 import ModeTalkElse2
from .modemenu import ModeMenu


class ModeMenu2(ModeMenu):
    def _handleLoad(self):
        super()._handleLoad()
        # if self._convo_key == "1":
        #     if shared.state.protag_mon.personality == Personality.Affectionate:
        #         self._text = "Thanks for helping me win that fight!"
        #     elif shared.state.protag_mon.personality == Personality.Aggressive:
        #         self._text = "Okay, we need to go do that again!"
        #     elif shared.state.protag_mon.personality == Personality.Careful:
        #         self._text = "That was a little scary, but so cool!"
        #     elif shared.state.protag_mon.personality == Personality.Energetic:
        #         self._text = "That was exciting!"
        # elif self._convo_key == "3a1":
        #     if shared.state.protag_mon.personality == Personality.Affectionate:
        #         self._text = "Thanks for helping me!"
        #     elif shared.state.protag_mon.personality == Personality.Aggressive:
        #         self._text = "We'll get them good!"
        #     elif shared.state.protag_mon.personality == Personality.Careful:
        #         self._text = "Help me out again, okay?"
        #     elif shared.state.protag_mon.personality == Personality.Energetic:
        #         self._text = "We've got this!"

    def _handleButton(self, prev_convo_key, index):
        if prev_convo_key == "xxx":
            self._stopMixer()
            self.next_mode = ModeFight(
                shared.state.protag_mon,
                Monster.atLevel(2),
                lambda: ModeTalkWin2() if shared.state.fight_results[-1] == 1 else ModeTalkElse2()
            )
            return True
        return False
