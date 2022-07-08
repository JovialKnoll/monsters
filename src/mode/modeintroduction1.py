import jovialengine

from personality import Personality
from .modeconvo import ModeConvo


class ModeIntroduction1(ModeConvo):
    def _handleLoad(self):
        if self._convo_key == "0":
            personality = jovialengine.getGame().state.protag_mon.personality
            if personality == Personality.Affectionate:
                self._text = "Hello! :)"
            elif personality == Personality.Aggressive:
                self._text = "You're finally here?"
            elif personality == Personality.Careful:
                self._text = "H-hi."
            elif personality == Personality.Energetic:
                self._text = "Hi!"
