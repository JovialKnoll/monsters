class Mood(object):
    # So instead of using numbers/strings/whatever for moods, just use Mood.the_mood
    # This way, if something is mistyped or whatever we will get an error, useful.
    class Neutral(object):
        drvChange = 0

    class Bored(object):
        drvChange = -1

    class Sad(object):
        drvChange = -1

    class Angry(object):
        drvChange = 1

    class Happy(object):
        drvChange = 1
