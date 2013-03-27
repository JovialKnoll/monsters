from feelings import *
class Monster(object):
    drv_max = 4
    lvl_max = 3
    
    @classmethod
    def atLevel(cls, in_lvl, in_stats={}):
        """Create a new monster at a given level not above the maximum level, setting stats, etc. as needed."""
        new_mon = cls(in_stats)
        for n in range(min(in_lvl,cls.lvl_max)):
            new_mon.levelUp()
        return new_mon
    
    def __init__(self, in_stats={}):
        """Create a new monster, setting stats, etc. as needed."""
        self.lvl = 0
        self.awr = 0
        self.personality = Personality.random()
        self.mood = Mood.neutral
        self.stats = {x: 4 for x in ('hpm', 'hpc', 'atk', 'def', 'spd')}
        self.stats['drv'] = Monster.drv_max/2
        self.stats[self.personality.stat] += 1
        #above line will be replaced with more specific stat generation, instead of mostly 1's everywhere
        self.stats.update(in_stats)
        #the look of the monster should be set, too...
        
    def levelUp(self):
        """Level up a monster, setting stats, etc. as needed."""
        if self.lvl >= Monster.lvl_max:
            return 0
        self.lvl += 1
        #change other stats as appropriate here...
        #change the look as appropriate here...
        return 1