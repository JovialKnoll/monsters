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
        personality = jovialengine.game.getInstance().state.protag_mon.personality
        if self._convo_key == "1":
            if personality == Personality.Affectionate:
                self._text = "Thanks for helping me win that fight!"
            elif personality == Personality.Aggressive:
                self._text = "Okay, we need to go do that again!"
            elif personality == Personality.Careful:
                self._text = "That was a little scary, but so cool!"
            elif personality == Personality.Energetic:
                self._text = "That was exciting!"
        elif self._convo_key == "3a1":
            if personality == Personality.Affectionate:
                self._text = "Thanks for helping me!"
            elif personality == Personality.Aggressive:
                self._text = "We'll get them good!"
            elif personality == Personality.Careful:
                self._text = "Help me out again, okay?"
            elif personality == Personality.Energetic:
                self._text = "We've got this!"

    def _handleButton(self, prev_convo_key, index):
        if prev_convo_key == "3a1":
            self._stopMixer()
            self.next_mode = ModeFight(
                jovialengine.game.getInstance().state.protag_mon,
                Monster.atLevel(1),
                lambda: ModeTalkWin1() if jovialengine.game.getInstance().state.fight_results[-1] == 1 else ModeTalkElse1()
            )
            return True
        return False
