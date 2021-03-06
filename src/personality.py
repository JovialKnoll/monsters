import random

class Personality(object):
    # Passing around classes instead of strings or something, sort of like an enum.
    class Affectionate(object):
        stat = 'vit'

    class Aggressive(object):
        stat = 'atk'

    class Careful(object):
        stat = 'def'

    class Energetic(object):
        stat = 'spd'

    @classmethod
    def random(cls):
        """Return a random personality."""
        return random.choice((cls.Affectionate, cls.Aggressive, cls.Careful, cls.Energetic))

    @classmethod
    def generateName(cls, mon_personality):
        """Generate a name for a monster."""
        # fill in with unique syllables
        if mon_personality in (cls.Affectionate, cls.Careful):
            temp_name = random.choice(("Fa","Ji","Sy","Ba","Vi","Pho")) + random.choice(("la","lo","mog","ta"))
        else:# cls.Aggressive, cls.Energetic
            temp_name = random.choice(("Ga","Ku","Zi","Ru","Te","The")) + random.choice(("va","iy","na","ran"))
        return temp_name + random.choice(("ex","ul","av","em","ix","ab","ev","og","za","el"))
