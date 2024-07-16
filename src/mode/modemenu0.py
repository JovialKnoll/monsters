import jovialengine

from monster import Monster
from personality import Personality
from .modefight import ModeFight
from .modetalkwin0 import ModeTalkWin0
from .modetalkelse0 import ModeTalkElse0
from .modemenu import ModeMenu


class ModeMenu0(ModeMenu):
    def _handle_load(self):
        super()._handle_load()
        if self._convo_key == "3a3":
            personality = jovialengine.get_state().protag_mon.personality
            if personality == Personality.Affectionate:
                self._text = "I'm sure we'll do great."
            elif personality == Personality.Aggressive:
                self._text = "Let's go win a fight!"
            elif personality == Personality.Careful:
                self._text = "Be careful, okay?"
            elif personality == Personality.Energetic:
                self._text = "I'm so excited!"

    def _handle_button(self, prev_convo_key, index):
        if prev_convo_key == "3a3":
            self._stop_mixer()
            self.next_mode = ModeFight(
                jovialengine.get_state().protag_mon,
                Monster.at_level(0),
                lambda: ModeTalkWin0() if jovialengine.get_state().fight_results[-1] == 1 else ModeTalkElse0()
            )
            return True
        return False
