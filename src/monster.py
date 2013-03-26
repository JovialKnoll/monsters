
class Monster(object):
    drv_max = 6#arbitrary values for now
    def __init__(self, level=0):
        """Create a new monster, setting stats as needed."""
        self.stats = dict({x: 1 for x in ('hpm', 'hpc', 'atk', 'def', 'spd')}, **{'drv': drv_max/2})
        #more stats and stuff needed