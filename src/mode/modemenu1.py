import jovialengine

from monster import Monster
from personality import Personality
from .modefight import ModeFight
from .modetalkwin1 import ModeTalkWin1
from .modetalkelse1 import ModeTalkElse1
from .modemenu import ModeMenu


class ModeMenu1(ModeMenu):
    def _handleLoad(self):
        super()._handleLoad()
        if self._convo_key == "1":
            if jovialengine.shared.state.protag_mon.personality == Personality.Affectionate:
                self._text = "Thanks for helping me win that fight!"
            elif jovialengine.shared.state.protag_mon.personality == Personality.Aggressive:
                self._text = "Okay, we need to go do that again!"
            elif jovialengine.shared.state.protag_mon.personality == Personality.Careful:
                self._text = "That was a little scary, but so cool!"
            elif jovialengine.shared.state.protag_mon.personality == Personality.Energetic:
                self._text = "That was exciting!"
        elif self._convo_key == "3a1":
            if jovialengine.shared.state.protag_mon.personality == Personality.Affectionate:
                self._text = "Thanks for helping me!"
            elif jovialengine.shared.state.protag_mon.personality == Personality.Aggressive:
                self._text = "We'll get them good!"
            elif jovialengine.shared.state.protag_mon.personality == Personality.Careful:
                self._text = "Help me out again, okay?"
            elif jovialengine.shared.state.protag_mon.personality == Personality.Energetic:
                self._text = "We've got this!"

    def _handleButton(self, prev_convo_key, index):
        if prev_convo_key == "3a1":
            self._stopMixer()
            self.next_mode = ModeFight(
                jovialengine.shared.state.protag_mon,
                Monster.atLevel(1),
                lambda: ModeTalkWin1() if jovialengine.shared.state.fight_results[-1] == 1 else ModeTalkElse1()
            )
            return True
        return False
