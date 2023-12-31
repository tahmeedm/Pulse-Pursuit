import random

def Flashlightfail():
    return True

def Shadowrun():
    return True

def Soundspook():
    # Randomly Picks a sound file index
    spook_sounds = [0, 1, 2, 3, 4]
    random_sound_index = random.choice(spook_sounds)

    return random_sound_index

def Choose_Event():
    # Probability weights for each item
    weights = [0.20, 0.1, 0.70]

    rand_value = random.random()
    cumulative_weight = 0
    random_index = 0

    for i, weight in enumerate(weights):
        cumulative_weight += weight
        if rand_value < cumulative_weight:
            random_index = i
            break
    return random_index

def scare():
    index = Choose_Event()
    random_sound_index = None  # Initialize the variable here

    if index == 0:
        status = Flashlightfail()

    elif index == 1:
        status = Shadowrun()

    elif index == 2:
        random_sound_index = Soundspook()
        status = True

    return [status, index, random_sound_index]

soundlist = [("lib/sounds/Spooky_sound1.mp3"),
             ("lib/sounds/Spooky_sound2.mp3"),
             ("lib/sounds/Spooky_sound3.mp3"),
             ("lib/sounds/Spooky_sound4.mp3"),
             ("lib/sounds/Spooky_sound5.mp3")]
