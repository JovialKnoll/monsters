import os, pygame, random
from feelings import *
from skin import *
random.seed()
class Monster(object):
    drv_max = 4
    lvl_max = 3
    sprite_size = (48,48)
    sprite_path = os.path.join('gfx', 'monster-parts')
    
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
        self.stats.update(in_stats)
        #the look of the monster should be set, too...
        self.skin = Skin.random(self.personality)
        #access the SkinTone with self.skin[self.lvl]
        self.sprite = pygame.Surface(Monster.sprite_size)
        #not entirely sure about the order for the next few lines
        self.sprite.blit(pygame.image.load(os.path.join(Monster.sprite_path, '0-body-'+random.choice(('A','B','C'))+'.png')), (0,0))
        self.sprite.blit(pygame.image.load(os.path.join(Monster.sprite_path, '0-head-'+random.choice(('A','B','C'))+'.png')), (0,0))
        self.sprite.blit(pygame.image.load(os.path.join(Monster.sprite_path, '0-legs-'+random.choice(('A','B','C'))+'.png')), (0,0))
        
        #convert after finishing stuff
        self.sprite.convert_alpha()
        
    def levelUp(self):
        """Level up a monster, setting stats, etc. as needed."""
        if self.lvl >= Monster.lvl_max:
            return 0
        self.lvl += 1
        #change other stats as appropriate here...
        #change the look as appropriate here...
        #for my own reference: tail->body->head->legs->arms
        return 1
        
    def draw(self, screen):
        screen.blit(self.sprite, (0,0))
        #just a test