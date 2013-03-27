class Monster(object):
    drv_max = 6#arbitrary value for now
    lvl_max = 5#arbitrary value for now
    
    @classmethod
    def atLevel(cls, in_lvl, in_stats={}):
        """Create a new monster at a given level not above the maximum level, setting stats, etc. as needed."""
        new_mon = cls(in_stats)
        for n in range(min(in_lvl,cls.lvl_max)):
            new_mon.levelUp()
        return new_mon
    
    def __init__(self, in_stats={}):
        """Create a new monster, setting stats, etc. as needed."""
        self.lvl = 0#starting at level 0, if that's fine
        self.stats = {x: 1 for x in ('hpm', 'hpc', 'atk', 'def', 'spd', 'awr')}
        self.stats['drv'] = Monster.drv_max/2
        #above line will be replaced with more specific stat generation, instead of mostly 1's everywhere
        #maybe we don't need seperate awr and lvl stats... depending on things
        self.stats.update(in_stats)
        self.personality = ""#placeholder lines for now
        self.mood = ""#yup
        #the look of the monster should be set, too...
        
    def levelUp(self):
        """Level up a monster, setting stats, etc. as needed."""
        if self.lvl >= Monster.lvl_max:
            return 0
        self.lvl += 1
        #change other stats as appropriate here...
        #change the look as appropriate here...
        return 1