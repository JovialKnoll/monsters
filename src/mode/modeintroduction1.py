import shared
from personality import Personality

from .modeconvo import ModeConvo


class ModeIntroduction1(ModeConvo):
    def _handleLoad(self):
        if self._convo_key == "0":
            if shared.state.protag_mon.personality == Personality.Affectionate:
                self._text = "Hello! :)"
            elif shared.state.protag_mon.personality == Personality.Aggressive:
                self._text = "You're finally here?"
            elif shared.state.protag_mon.personality == Personality.Careful:
                self._text = "H-hi."
            elif shared.state.protag_mon.personality == Personality.Energetic:
                self._text = "Hi!"
