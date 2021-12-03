import shared
from monster import Monster
from personality import Personality
from .modefight import ModeFight
from .modetalkwin0 import ModeTalkWin0
from .modetalkelse0 import ModeTalkElse0
from .modemenu import ModeMenu


class ModeMenu0(ModeMenu):
    def _handleLoad(self):
        super()._handleLoad()
        if self._convo_key == "3a3":
            if shared.state.protag_mon.personality == Personality.Affectionate:
                self._text = "I'm sure we'll do great."
            elif shared.state.protag_mon.personality == Personality.Aggressive:
                self._text = "Let's go win a fight!"
            elif shared.state.protag_mon.personality == Personality.Careful:
                self._text = "Be careful, okay?"
            elif shared.state.protag_mon.personality == Personality.Energetic:
                self._text = "I'm so excited!"

    def _handleButton(self, prev_convo_key, index):
        if prev_convo_key == "3a3":
            self._stopMixer()
            self.next_mode = ModeFight(
                shared.state.protag_mon,
                Monster.atLevel(0),
                lambda: ModeTalkWin0() if shared.state.fight_results[-1] == 1 else ModeTalkElse0()
            )
            return True
        return False
