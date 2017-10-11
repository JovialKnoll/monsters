import string
import pygame

from monconvomode import *

class MenuMode(MonConvoMode):
    def _textMain(self):
        mon = GameMode.shared['protag_mon']
        mon_string = "lvl: " + str(mon.lvl) + "\n"
        mon_string += " ".join([stat + ": " + str(mon.stats[stat]) for stat in mon.main_stats])
        mon_string += "\nhpm: " + str(mon.stats['hpm']) + "  "
        mon_string += "hpc: " + str(mon.stats['hpc']) + "  "
        mon_string += "drv: " + str(mon.stats['drv'])
        return mon.name + "\n" + mon_string.upper()

    def _textButton0(self):
        return "Wanna Talk?"
    def _textButton1(self):
        return "Look for Trouble"
    def _textButton2(self):
        # mmm, maybe something else here
        return "Time for a Checkup"
    def _textButton3(self):
        return "Take a Break"
    def _goButton0(self):
        print("Go to a convo?")
    def _goButton1(self):
        print("Go to a fight?")
    def _goButton2(self):
        # uhhhh
        print("Something?")
    def _goButton3(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT, {}))
