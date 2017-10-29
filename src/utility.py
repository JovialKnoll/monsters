import random

def reduceNumber(number, divisor):
    result = number // divisor
    mod = number % divisor
    if random.random() < (mod / divisor):
        result += 1
    return result

def lerp(start, end, mix):
    return start + (end - start)*mix

def incSpeedLerp(start, end, mix):
    return lerp(start, end, mix**2)

def decSpeedLerp(start, end, mix):
    return lerp(start, end, 1 - (1 - mix)**2)

def incDecSpeedLerp(start, end, mix):
    midpoint = lerp(start, end, 0.5)
    if mix < 0.5:
        func = incSpeedLerp
        end = midpoint
        mix -= 0.5
    else:
        func = decSpeedLerp
        start = midpoint
    return func(start, end, mix*2)

def decIncSpeedLerp(start, end, mix):
    midpoint = lerp(start, end, 0.5)
    if mix < 0.5:
        func = decSpeedLerp
        end = midpoint
        mix -= 0.5
    else:
        func = incSpeedLerp
        start = midpoint
    return func(start, end, mix*2)
