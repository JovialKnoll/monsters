import os
import random
import uuid
import math

import pygame
import jovialengine

import constants
from personality import Personality
from skin import Skin


class Monster(jovialengine.AnimSprite):
    DRV_MAX = 4
    LVL_MAX = 3
    MAIN_STATS = (
        'atk',
        'def',
        'spd',
        'vit',
    )
    BODY_SECTIONS = (
        'tail',
        'body',
        'head',
        'legs',
        'arms',
    )

    __slots__ = (
        'uuid',
        'lvl',
        'personality',
        'name',
        'skin',
        'stats',
        'sprite_groups',
        'sprite_files',
        'old_sprite_files',
        'sprite',
        'sprite_right',
        'facing_right',
    )

    def __init__(self, in_stats: dict = None):
        """Create a new monster, setting stats, etc. as needed."""
        super().__init__()
        self.uuid = str(uuid.uuid4())
        self.lvl = 0
        self.personality = Personality.random()
        self.name = Personality.generateName(self.personality)
        self.skin = Skin.random(self.personality)

        self.stats = {x: 2 for x in self.MAIN_STATS}
        self.stats['drv'] = self.DRV_MAX
        self._levelStats()
        if in_stats is not None:
            self.stats.update(in_stats)
        self.setHealth()

        self.rect = pygame.Rect(0, 0, 48, 48)
        self.sprite_groups = tuple(random.choice(('A', 'B', 'C')) for _ in range(5))
        self.sprite_files = None
        self._setSpritePaths()
        self.old_sprite_files = []
        self._setSprites()
        self.setImage()

    def save(self):
        return {
            'super': super().save(),
            'uuid': self.uuid,
            'lvl': self.lvl,
            'personality': self.personality,
            'name': self.name,
            'skin': self.skin,
            'stats': self.stats,
            'sprite_groups': self.sprite_groups,
            'sprite_files': self.sprite_files,
            'old_sprite_files': self.old_sprite_files,
            'facing_right': self.facing_right,
        }

    @classmethod
    def load(cls, save_data):
        new_obj = cls()
        new_obj.uuid = save_data['uuid']
        new_obj.lvl = save_data['lvl']
        new_obj.personality = save_data['personality']
        new_obj.name = save_data['name']
        new_obj.skin = save_data['skin']
        new_obj.stats = save_data['stats']
        new_obj.sprite_groups = save_data['sprite_groups']
        new_obj.sprite_files = save_data['sprite_files']
        new_obj.old_sprite_files = save_data['old_sprite_files']
        new_obj._setSprites()
        new_obj.setImage(save_data['facing_right'])

        super_obj = super().load(save_data['super'])
        new_obj.rect.topleft = super_obj.rect.topleft
        new_obj.anims = super_obj.anims
        new_obj.last_pos = super_obj.last_pos
        new_obj.time = super_obj.time

        return new_obj

    def fightStart(self):
        self.stats['drv'] = self.DRV_MAX
        if self.lvl == 0:
            self.stats['drv'] -= 1
        self.setHealth()

    def _drvEffect(self):
        return self.stats['drv'] - self.DRV_MAX + 2

    def _getHealthBasis(self):
        return 8 + (self.lvl * 2 + 1)**2

    def fightHit(self, action: str, is_protag: bool = False):
        hit = 0
        block = 0
        if action == constants.FIGHT_ATTACK:
            hit = self.stats['atk'] // 2 + self.stats['spd'] // 2
            block = hit + random.randint(0, 1)
        elif action == constants.FIGHT_DEFEND:
            hit = self.stats['vit'] // 2 + self.stats['def'] // 2
            block = hit + random.randint(0, 1)
        # DODGE
        else:
            hit = self.stats['atk'] // 4 + self.stats['vit'] // 4
            block = self.stats['def'] // 2 + self.stats['spd'] // 2 + random.randint(0, 1)
        if action == self.personality.preferred_action:
            bonus = self._getHealthBasis() // 3
            if is_protag:
                bonus = self._getHealthBasis() // 2
            hit += bonus
            block += bonus
        else:
            hit -= self._getHealthBasis() // 4 + random.randint(1, 2)
        hit = max(hit + random.randint(-1, 1) + self._drvEffect(), 0)
        block = max(block + random.randint(-1, 1) + self._drvEffect(), 0)
        self.stats['drv'] = max(self.stats['drv'] - 1, 0)
        return hit, block

    def _levelStats(self):
        for stat in self.MAIN_STATS:
            self.stats[stat] += 2
        for stat in random.sample(self.MAIN_STATS, 2):
            self.stats[stat] += 1
        self.stats[self.personality.stat] += 2

    def setHealth(self):
        self.stats['hpm'] = self._getHealthBasis() + self.stats['vit']
        self.stats['hpc'] = self.stats['hpm']

    def _getSpritePath(self, section: str, group: str):
        part = ''
        if self.lvl > 0:
            part = random.randint(0, 2)
        return '{}-{}-{}{}.png'.format(self.lvl, section, group, part)

    def _setSpritePaths(self):
        self.sprite_files = tuple(
            self._getSpritePath(self.BODY_SECTIONS[i], self.sprite_groups[i]) for i in range(5)
        )
        if self.lvl == 0:
            self.sprite_files = self.sprite_files[1:4]

    @staticmethod
    def _loadSpriteFile(sprite_file: str):
        return pygame.image.load(
            os.path.join(constants.MONSTER_PARTS_DIRECTORY, sprite_file)
        )

    def _setSprites(self, alt_lvl=None, alt_sprite_files=None):
        lvl = self.lvl
        sprite_files = self.sprite_files
        if alt_lvl is not None and alt_sprite_files is not None:
            lvl = alt_lvl
            sprite_files = alt_sprite_files
        self.sprite = self._loadSpriteFile(sprite_files[0]).convert()
        self.sprite.set_colorkey(constants.COLORKEY)
        for sprite_path in sprite_files[1:]:
            new_part = self._loadSpriteFile(sprite_path)
            new_part.set_colorkey(constants.COLORKEY)
            self.sprite.blit(new_part, (0, 0))
        if lvl > 0:
            pix_array = pygame.PixelArray(self.sprite)
            pix_array.replace(
                self.skin[0].dark,
                self.skin[lvl].dark
            )
            pix_array.replace(
                self.skin[0].light,
                self.skin[lvl].light
            )
            del pix_array
        self.sprite_right = pygame.transform.flip(self.sprite, True, False)

    def getBarColor(self):
        return self.skin[self.lvl].light

    def getBarColor2(self):
        return self.skin[self.lvl].dark

    def setImage(self, face_right=False):
        self.facing_right = face_right
        if face_right:
            self.image = self.sprite_right
        else:
            self.image = self.sprite
        standing_pos = self.rect.midbottom
        self.rect = self.image.get_rect()
        self.rect.midbottom = standing_pos

    def levelUp(self):
        """Level up a monster, setting stats, etc. as needed."""
        if self.lvl >= self.LVL_MAX:
            return False
        self.lvl += 1
        self._levelStats()
        self.stats['drv'] = self.DRV_MAX
        self.setHealth()
        self.old_sprite_files.append(self.sprite_files)
        self._setSpritePaths()
        self._setSprites()
        self.setImage()
        return True

    @staticmethod
    def _getSpacing(stat_num: int):
        return (2 - math.ceil(math.log10(stat_num))) * "_"

    def getStatText(self):
        stat_text = f"lvl: {self.lvl}\n"
        stat_text += "_".join(
            [f"{stat}: {self.stats[stat]}" + self._getSpacing(self.stats[stat]) for stat in self.MAIN_STATS]
        )
        stat_text += f"\ndrv: {self.stats['drv']}/{self.DRV_MAX}"
        stat_text += f"\n_hp: {self.stats['hpc']}/{self.stats['hpm']}"
        return self.name + "\n" + stat_text.upper()

    def getCard(self):
        card = pygame.Surface((64 * 4, 64 * 2))
        card.fill(constants.WHITE)
        rect = self.sprite_right.get_rect()
        rect.midbottom = (64 // 2 + 64 * self.lvl, 64)
        card.blit(self.sprite_right, rect)
        for lvl, sprite_files in enumerate(self.old_sprite_files):
            self._setSprites(lvl, sprite_files)
            rect = self.sprite_right.get_rect()
            rect.midbottom = (64 // 2 + 64 * lvl, 64)
            card.blit(self.sprite_right, rect)
        self._setSprites()
        jovialengine.shared.font_wrap.renderToInside(
            card,
            (0, 64 + (64 - constants.FONT_HEIGHT * 5) // 2),
            64 * 4,
            self.getStatText(),
            False,
            constants.BLACK
        )
        jovialengine.shared.font_wrap.renderToInside(
            card,
            (0, 0),
            64 * 4,
            constants.TITLE,
            False,
            constants.TEXT_COLOR
        )
        website = "jovialknoll.itch.io"
        website_width = len(website) * constants.FONT_SIZE
        jovialengine.shared.font_wrap.renderToInside(
            card,
            (64 * 4 - website_width, 64 * 2 - constants.FONT_HEIGHT),
            website_width,
            website,
            False,
            constants.TEXT_COLOR
        )
        return card

    @classmethod
    def atLevel(cls, in_lvl, in_stats: dict = None):
        """Create a new monster at a given level not above the maximum level, setting stats, etc. as needed."""
        new_mon = cls(in_stats)
        for n in range(min(in_lvl, cls.LVL_MAX)):
            new_mon.levelUp()
        return new_mon
