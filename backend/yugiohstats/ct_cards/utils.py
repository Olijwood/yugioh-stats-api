
def parse_yugioh_rarity(rarity, set_code):

    if 'Rare | ' in rarity:
        rarity = rarity.split(' |')[0]
    if ' - Misprint' in rarity:
        rarity = rarity.split(' - Misprin')[0]
    if ' | Alternate Art' in rarity:
        rarity = rarity.replace(' | Alternate Art', '')
    if ' | Alternative Art' in rarity:
        rarity = rarity.replace(' | Alternative Art', '')
    if "Collector's" in rarity:
        rarity = rarity.replace("Collector's", 'Collectors')
    if set_code == 'ra02' or set_code == 'ra01':
        if 'Ultimate' in rarity:
            rarity = 'Prismatic Ultimate Rare'
        if 'Collector' in rarity:
            rarity = 'Prismatic Collectors Rare'
        if 'Quarter' in rarity:
            rarity = 'Quarter Century Secret Rare'
        if 'Platinum' in rarity:
            rarity = 'Platinum Secret Rare'
        if 'Ultra' in rarity:
            rarity = 'Ultra Rare'
        if 'Super' in rarity:
            rarity = 'Super Rare'
    if set_code == 'bach' and rarity == 'Promo':
            rarity = 'Secret Rare'
    return rarity