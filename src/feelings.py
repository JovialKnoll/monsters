import random
random.seed()
class Personality(object):
    #Passing around classes instead of strings or something, sort of like an enum.
    class Affectionate(object):
        stat = 'hpm'
    
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
        
class Mood(object):
    #So instead of useing numbers/strings/whatever for moods, just use Mood.the_mood
    #This way, if something is mistyped or whatever we will get an error, useful.
    neutral = 0
    bored = 1
    sad = 2
    angry = 3
    happy = 4
    