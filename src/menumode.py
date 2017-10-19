import pygame

import shared
from monconvomode import MonConvoMode

class MenuMode(MonConvoMode):
    __slots__ = (
    )

    def _textMain(self):
        mon = shared.state.protag_mon
        mon_string = "lvl: " + str(mon.lvl) + "\n"
        mon_string += " ".join([stat + ": " + str(mon.stats[stat]) for stat in mon.main_stats])
        mon_string += "\nhpm: " + str(mon.stats['hpm']) + "  "
        mon_string += "hpc: " + str(mon.stats['hpc']) + "  "
        mon_string += "drv: " + str(mon.stats['drv'])
        return mon.name + "\n" + mon_string.upper()

    def _textButton(self, index):
        if index == 0:
            return "Wanna Talk?"
        elif index == 1:
            return "Look for Trouble"
        elif index == 2:
            # mmm, maybe something else here
            return "Time for a Checkup"
        elif index == 3:
            return "Take a Break"
    def _goButton(self, index):
        if index == 0:
            print("Go to a convo?")
        elif index == 1:
            print("Go to a fight?")
        elif index == 2:
            # uhhhh
            print("Something?")
        elif index == 3:
            pygame.event.post(pygame.event.Event(pygame.QUIT, {}))
