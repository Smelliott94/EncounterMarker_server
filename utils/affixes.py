AFFIXES = {
    1: 'Overflowing',
    2: 'Skittish',
    3: 'Volcanic',
    4: 'Necrotic',
    5: 'Teeming',
    6: 'Raging',
    7: 'Bolstering',
    8: 'Sanguine',
    9: 'Tyrannical',
    10: 'Fortified',
    11: 'Bursting',
    12: 'Grievous',
    13: 'Explosive',
    14: 'Quaking',
    16: 'Infested',
    117: 'Reaping',
    119: 'Beguiling',
    120: 'Awakened',
    121: 'Prideful',
    122: 'Inspiring',
    123: 'Spiteful',
    124: 'Storming',
    128: 'Tormented',
    129: 'Infernal',
    130: 'Encrypted',
    131: 'Shrouded',
    132: 'Thundering'
}

def get_affixes(codes):
    affixes = []
    for number in codes:
        affixes.append(AFFIXES[number])
    return ' '.join(affixes)