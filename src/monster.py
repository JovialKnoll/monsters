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
        
        self.skin = Skin.random(self.personality)
        #access the SkinTone with self.skin[self.lvl]
        self.sprite_groups = [random.choice(('A','B','C')) for x in range(5)]
        self.sprite = pygame.image.load(os.path.join(Monster.sprite_path, '0-body-'+self.sprite_groups[1]+'.png'))
        self.sprite.blit(pygame.image.load(os.path.join(Monster.sprite_path, '0-head-'+self.sprite_groups[2]+'.png')), (0,0))
        self.sprite.blit(pygame.image.load(os.path.join(Monster.sprite_path, '0-legs-'+self.sprite_groups[3]+'.png')), (0,0))
        self.sprite.convert_alpha()
        
    def levelUp(self):
        """Level up a monster, setting stats, etc. as needed."""
        if self.lvl >= Monster.lvl_max:
            return 0
        self.lvl += 1
        #change other stats as appropriate here...
        #change the look as appropriate here...
        #for my own reference: tail->body->head->legs->arms
        self.sprite = pygame.image.load(os.path.join(Monster.sprite_path, str(self.lvl)+'-tail-'+self.sprite_groups[0]+str(random.randint(0,2))+'.png'))
        self.sprite.blit(pygame.image.load(os.path.join(Monster.sprite_path, str(self.lvl)+'-body-'+self.sprite_groups[1]+str(random.randint(0,2))+'.png')), (0,0))
        self.sprite.blit(pygame.image.load(os.path.join(Monster.sprite_path, str(self.lvl)+'-head-'+self.sprite_groups[2]+str(random.randint(0,2))+'.png')), (0,0))
        self.sprite.blit(pygame.image.load(os.path.join(Monster.sprite_path, str(self.lvl)+'-legs-'+self.sprite_groups[3]+str(random.randint(0,2))+'.png')), (0,0))
        self.sprite.blit(pygame.image.load(os.path.join(Monster.sprite_path, str(self.lvl)+'-arms-'+self.sprite_groups[4]+str(random.randint(0,2))+'.png')), (0,0))
        #color stuff here
        self.sprite.convert_alpha()
        return 1
        
    def draw(self, screen):
        screen.blit(self.sprite, (104,104))
        #just a test