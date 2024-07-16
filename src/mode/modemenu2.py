import jovialengine

from monster import Monster
from personality import Personality
from .modefight import ModeFight
from .modetalkwin2 import ModeTalkWin2
from .modetalkelse2 import ModeTalkElse2
from .modemenu import ModeMenu


class ModeMenu2(ModeMenu):
    def _handle_load(self):
        super()._handle_load()
        if self._convo_key == "2":
            personality = jovialengine.get_state().protag_mon.personality
            if personality == Personality.Affectionate:
                self._text = "Happy and healthy."
            elif personality == Personality.Aggressive:
                self._text = "Ready to win again."
            elif personality == Personality.Careful:
                self._text = "Probably ready to go."
            elif personality == Personality.Energetic:
                self._text = "Excited and ready."

    def _handle_button(self, prev_convo_key, index):
        if prev_convo_key == "3a":
            self._stop_mixer()
            self.next_mode = ModeFight(
                jovialengine.get_state().protag_mon,
                Monster.at_level(2),
                lambda: ModeTalkWin2() if jovialengine.get_state().fight_results[-1] == 1 else ModeTalkElse2()
            )
            return True
        return False
