import os, pygame, random
from skin import *
from feelings import *
random.seed()
class Monster(object):
    drv_max = 4
    lvl_max = 3
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
        self.sprite_size = (48,48)
        self.lvl = 0
        self.awr = 0#awareness, this is a thing for conversations / progress through the game
        #it might make more sense to hold info for conversations flow in GameMode.shared, but I'm not sure
        #depends on how this number interacts with monster stuff
        self.personality = Personality.random()
        self.mood = Mood.neutral#mood might only be changed by and do stuff during battles / convos? maybe
        self.stats = {x: 4 for x in ('hpm', 'atk', 'def', 'spd')}
        self.stats['drv'] = Monster.drv_max//2
        self.stats[self.personality.stat] += 1
        self.stats['hpc'] = self.stats['hpm']
        self.stats.update(in_stats)
        
        self.name = Personality.generateName(self.personality)
        
        self.skin = Skin.random(self.personality)
        #access the SkinTone with self.skin[self.lvl]
        self.sprite_groups = [random.choice(('A','B','C')) for x in range(5)]
        self.sprite =    pygame.image.load(os.path.join(Monster.sprite_path, '0-body-'+self.sprite_groups[1]+'.png'))
        self.sprite.blit(pygame.image.load(os.path.join(Monster.sprite_path, '0-head-'+self.sprite_groups[2]+'.png')), (0,0))
        self.sprite.blit(pygame.image.load(os.path.join(Monster.sprite_path, '0-legs-'+self.sprite_groups[3]+'.png')), (0,0))
        self._finishSprite()
        
    def _finishSprite(self):
        #self.sprite_size = (64,64)
        #self.sprite = pygame.Surface((64,64))
        #self.sprite.fill((255,0,0))
        self.sprite = self.sprite.convert_alpha()
        self.sprite_right = pygame.transform.flip(self.sprite, True, False)
        
    def levelUp(self):
        """Level up a monster, setting stats, etc. as needed."""
        if self.lvl >= Monster.lvl_max:
            return 0
        self.lvl += 1
        if self.lvl > 2:
            self.sprite_size = (64,64)
        #change other stats as appropriate here...
        self.stats['hpc'] = self.stats['hpm']
        #sprite construction stuff
        self.sprite =    pygame.image.load(os.path.join(Monster.sprite_path, str(self.lvl)+'-tail-'+self.sprite_groups[0]+str(random.randint(0,2))+'.png'))
        self.sprite.blit(pygame.image.load(os.path.join(Monster.sprite_path, str(self.lvl)+'-body-'+self.sprite_groups[1]+str(random.randint(0,2))+'.png')), (0,0))
        self.sprite.blit(pygame.image.load(os.path.join(Monster.sprite_path, str(self.lvl)+'-head-'+self.sprite_groups[2]+str(random.randint(0,2))+'.png')), (0,0))
        self.sprite.blit(pygame.image.load(os.path.join(Monster.sprite_path, str(self.lvl)+'-legs-'+self.sprite_groups[3]+str(random.randint(0,2))+'.png')), (0,0))
        self.sprite.blit(pygame.image.load(os.path.join(Monster.sprite_path, str(self.lvl)+'-arms-'+self.sprite_groups[4]+str(random.randint(0,2))+'.png')), (0,0))
        #color swapping stuff
        pix_array = pygame.PixelArray(self.sprite)
        pix_array.replace(self.skin[0].dark, self.skin[self.lvl].dark)
        pix_array.replace(self.skin[0].light, self.skin[self.lvl].light)
        del pix_array
        self._finishSprite()
        return 1
        
    def drawCentered(self, screen, pos, right=False):
        """Draw the monster on the screen, with its center at the position passed."""
        self.draw(screen, (pos[0]-self.sprite_size[0]//2, pos[1]-self.sprite_size[1]//2), right)
        
    def drawStanding(self, screen, pos, right=False):
        """Draw the monster on the screen, with its bottom-center at the position passed."""
        self.draw(screen, (pos[0]-self.sprite_size[0]//2, pos[1]-self.sprite_size[1]), right)
        
    def draw(self, screen, pos, right=False):
        """Draw the monster on the screen."""
        screen.blit(self.sprite if not right else self.sprite_right, pos)
        