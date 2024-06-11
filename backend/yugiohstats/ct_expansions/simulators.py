import random

def simulate_multiple_core_boxes(qcr_core_set_list, num_iterations):
    results = []
    for _ in range(num_iterations):
        result = get_simulated_total_for_qcr_core_set(qcr_core_set_list)
        results.append(result)
    return results

def get_simulated_total_for_qcr_core_set(qcr_core_set_list):
    set_qcr_prices = [card[1] for card in qcr_core_set_list if card[0] == 'Quarter Century Secret Rare']
    set_secret_prices = [card[1] for card in qcr_core_set_list if card[0] == 'Secret Rare']
    set_ultra_prices = [card[1] for card in qcr_core_set_list if card[0] == 'Ultra Rare']
    set_super_prices = [card[1] for card in qcr_core_set_list if card[0] == 'Super Rare']

    # Get random samples of prices for each rarity
    super_total = random.choices(set_super_prices, k=18)
    ultra_total = random.choices(set_ultra_prices, k=4)
    secret_total = random.choices(set_secret_prices, k=2)

    # Determine if the booster box contains a Quarter Century Rare
    if random.randint(1, 4) == 1:
        qcr = random.choice(set_qcr_prices)
        # Replace Ultra or Secret with QCR
        if random.randint(1, 2) == 1:
            ultra_total[-1] = qcr
        else:
            secret_total[-1] = qcr

    # Calculate the total booster value
    total = sum(super_total) + sum(ultra_total) + sum(secret_total)
    return round(total, 2)

def simulate_multiple_ra02_boxes(parsed_ra02, num_iterations):
    results = []
    
    for _ in range(num_iterations):
            
            result = ra02_get_simulated_booster_total(parsed_ra02)
            results.append(result)
    return results

def ra02_get_simulated_booster_total(parsed_rarity_ii):
    total = 0
    
    set_qcr_prices = [card[1] for card in parsed_rarity_ii if card[0] == 'Quarter Century Secret Rare']
    set_pcr_prices = [card[1] for card in parsed_rarity_ii if card[0] == 'Prismatic Collectors Rare']
    set_pur_prices = [card[1] for card in parsed_rarity_ii if card[0] == 'Prismatic Ultimate Rare']
    set_ps_prices = [card[1] for card in parsed_rarity_ii if card[0] == "Platinum Secret Rare"]
    set_secret_prices = [card[1] for card in parsed_rarity_ii if card[0] == "Secret Rare"]
    set_ultra_prices = [card[1] for card in parsed_rarity_ii if card[0] == "Ultra Rare"]
    set_super_prices = [card[1] for card in parsed_rarity_ii if card[0] == "Super Rare"]

    for _ in range(24):  # 24 packs per booster box
        pack_total = 0
        
        # Super * 3 per pack
        pack_total += sum(random.choices(set_super_prices, k=3))
        
        # Ultra * 4 per pack (1-in-6 chance each of being a Collector's Rare or Ultimate Rare)
        for _ in range(4):
            if random.randint(1, 6) == 1:
                if random.randint(1, 2) == 1:
                    pack_total += random.choice(set_pcr_prices)
                else:
                    pack_total += random.choice(set_pur_prices)
            else:
                pack_total += random.choice(set_ultra_prices)

        # Secret * 2 per pack (1 in 4 chance of being platinum or qcr)
        for _ in range(2):
            if random.randint(1, 4) == 1:
                if random.randint(1, 2) == 1:
                    pack_total += random.choice(set_qcr_prices)
                else:
                    pack_total += random.choice(set_ps_prices)
            else:
                pack_total += random.choice(set_secret_prices)
        
        total += pack_total
    
    return total

def simulate_multiple_ra01_boxes(parsed_ra02, num_iterations):
    results = []
    
    for _ in range(num_iterations):
            result = ra01_get_simulated_booster_total(parsed_ra02)
            results.append(result)

    return results


def ra01_get_simulated_booster_total(parsed_rarity_collection):
    total = 0
    
    set_qcr_prices = [card[1] for card in parsed_rarity_collection if card[0] == 'Quarter Century Secret Rare']
    set_pcr_prices = [card[1] for card in parsed_rarity_collection if card[0] == 'Prismatic Collectors Rare']
    set_pur_prices = [card[1] for card in parsed_rarity_collection if card[0] == 'Prismatic Ultimate Rare']
    set_ps_prices = [card[1] for card in parsed_rarity_collection if card[0] == "Platinum Secret Rare"]
    set_secret_prices = [card[1] for card in parsed_rarity_collection if card[0] == "Secret Rare"]
    set_ultra_prices = [card[1] for card in parsed_rarity_collection if card[0] == "Ultra Rare"]
    set_super_prices = [card[1] for card in parsed_rarity_collection if card[0] == "Super Rare"]

    for _ in range(24):  # 24 packs per booster box
        pack_total = 0
        
        # Super * 2 per pack
        pack_total += sum(random.choices(set_super_prices, k=2))
        
        # Ultra * 2 per pack (1-in-6 chance each of being a Collector's Rare or Ultimate Rare)
        for _ in range(2):
            if random.randint(1, 6) == 1:
                if random.randint(1, 2) == 1:
                    pack_total += random.choice(set_pcr_prices)
                else:
                    pack_total += random.choice(set_pur_prices)
            else:
                pack_total += random.choice(set_ultra_prices)

        # Secret * 1 per pack (1 in 4 chance of being platinum or qcr)
        
        if random.randint(1, 4) == 1:
            if random.randint(1, 2) == 1:
                pack_total += random.choice(set_qcr_prices)
            else:
                pack_total += random.choice(set_ps_prices)
        else:
            pack_total += random.choice(set_secret_prices)
        
        total += pack_total
    
    return total

def simulate_multiple_collector_without_qcr_boxes(parsed_collector, num_iterations):
    results = []
    
    for _ in range(num_iterations):
            result = collectors_set_noqcr_get_booster_total(parsed_collector)
            results.append(result)

    return results

def collectors_set_noqcr_get_booster_total(parsed_collector):
    total = 0

    set_collector_prices = [card[1] for card in parsed_collector if card[0] == "Collectors Rare"]
    set_ultra_prices = [card[1] for card in parsed_collector if card[0] == "Ultra Rare"]
    set_super_prices = [card[1] for card in parsed_collector if card[0] == "Super Rare"]

    # 24 packs per box
    # 3 ultra
    # 21 super
    
    ultra_count = 3
    super_count = 21

    # handle odds for Collector in booster box
    if random.randint(1, 3) == 1:
        if random.randint(1, 2) == 1:
            ultra_count -= 1
            total += random.choice(set_collector_prices)
        else:
            super_count -= 1
            total += random.choice(set_collector_prices)

        
    total += sum(random.choices(set_ultra_prices, k=ultra_count))
    total += sum(random.choices(set_super_prices, k=super_count))
    return total

def simulate_multiple_collector_with_qcr_boxes(parsed_collector, num_iterations):
    results = []
    
    for _ in range(num_iterations):
            result = collectors_set_qcr_get_booster_total(parsed_collector)
            results.append(result)

    return results

def collectors_set_qcr_get_booster_total(parsed_collector):
    total = 0

    set_qcr_prices = [card[1] for card in parsed_collector if card[0] == 'Quarter Century Secret Rare']
    set_collector_prices = [card[1] for card in parsed_collector if card[0] == "Collectors Rare"]
    set_ultra_prices = [card[1] for card in parsed_collector if card[0] == "Ultra Rare"]
    set_super_prices = [card[1] for card in parsed_collector if card[0] == "Super Rare"]

    # 24 packs per box
    # 3 ultra
    # 21 super
    
    ultra_count = 3
    super_count = 21

    # handle odds for Collector in booster box
    if random.randint(1, 3) == 1:
        if random.randint(1, 2) == 1:
            ultra_count -= 1
            total += random.choice(set_collector_prices)
        else:
            super_count -= 1
            total += random.choice(set_collector_prices)

    # handle odds for QCR in booster box
    if random.randint(1, 4) == 1:
        if random.randint(1, 2) == 1:
            ultra_count -= 1
            total += random.choice(set_qcr_prices)
        else:
            super_count -= 1
            total += random.choice(set_qcr_prices)
        
    total += sum(random.choices(set_ultra_prices, k=ultra_count))
    total += sum(random.choices(set_super_prices, k=super_count))
    return total

def simulate_multiple_bol_with_qcr_boxes(parsed_bol_qcr, num_iterations):
    results = []
    for _ in range(num_iterations):
        result = bol_qcr_get_booster_total(parsed_bol_qcr)
        results.append(result)
    return results

def bol_qcr_get_booster_total(parsed_bol_qcr):
    total = 0
    
    set_qcr_prices = [card[1] for card in parsed_bol_qcr if card[0] == 'Quarter Century Secret Rare']
    set_secret_prices = [card[1] for card in parsed_bol_qcr if card[0] == "Secret Rare"]
    set_ultra_prices = [card[1] for card in parsed_bol_qcr if card[0] == "Ultra Rare"]

    #24 packs per booster
    # 5 cards per pack, 4 ultra, 1 secret
    secret_count = 24
    ultra_count = 96

    #handle odds for qcr ( 1 in 4 boxes)
    if random.randint(1, 4) == 1:
        total += random.choice(set_qcr_prices)
        if random.randint(1, 2) == 1:
            secret_count -= 1
        else:
            ultra_count -= 1
        
    all_secret = random.choices(set_secret_prices, k=secret_count)
    secret = [price for price in all_secret if price >= 0.49]

    total += sum(secret)
    
    all_ultra = random.choices(set_ultra_prices, k=ultra_count)
    ultra = [price for price in all_ultra if price >= 0.49]

    total += sum(ultra)
    return round(total, 2)

def simulate_multiple_bol_with_starlight_boxes(parsed_bol_starlight, num_iterations):
    results = []
    for _ in range(num_iterations):
        result = bol_starlight_get_booster_total(parsed_bol_starlight)
        results.append(result)
    return results

def bol_starlight_get_booster_total(parsed_bol_starlight):
    total = 0
    
    set_starlight_prices = [card[1] for card in parsed_bol_starlight if card[0] == 'Starlight Rare']
    set_secret_prices = [card[1] for card in parsed_bol_starlight if card[0] == "Secret Rare"]
    set_ultra_prices = [card[1] for card in parsed_bol_starlight if card[0] == "Ultra Rare"]

    #24 packs per booster
    # 5 cards per pack, 4 ultra, 1 secret
    secret_count = 24
    ultra_count = 96

    #handle odds for starlight ( 1 in 12 boxes)
    if random.randint(1, 12) == 1:
        total += random.choice(set_starlight_prices)
        if random.randint(1, 2) == 1:
            secret_count -= 1
        else:
            ultra_count -= 1
        
    all_secret = random.choices(set_secret_prices, k=secret_count)
    secret = [price for price in all_secret if price >= 0.49]

    total += sum(secret)
    
    all_ultra = random.choices(set_ultra_prices, k=ultra_count)
    ultra = [price for price in all_ultra if price >= 0.49]

    total += sum(ultra)
    return round(total, 2)

def simulate_multiple_core_with_starlight_boxes(parsed_core_starlight, num_iterations):
    results = []
    for _ in range(num_iterations):
        result = core_starlight_get_booster_total(parsed_core_starlight)
        results.append(result)
    return results

def core_starlight_get_booster_total(parsed_core_starlight):
    total = 0
    
    set_starlight_prices = [card[1] for card in parsed_core_starlight if card[0] == 'Starlight Rare']
    set_secret_prices = [card[1] for card in parsed_core_starlight if card[0] == "Secret Rare"]
    set_ultra_prices = [card[1] for card in parsed_core_starlight if card[0] == "Ultra Rare"]
    set_super_prices = [card[1] for card in parsed_core_starlight if card[0] == "Super Rare"]

    #24 packs per booster #2 Secret, 4 ultra, 18 Super
    # 9 cards per pack, 1 holo, rest common/worthless

    secret_count = 2
    ultra_count = 4
    super_count = 18

    #handle odds for starlight ( 1 in 12 boxes)
    if random.randint(1, 12) == 1:
        total += random.choice(set_starlight_prices)
        if random.randint(1, 2) == 1:
            secret_count -= 1
        else:
            ultra_count -= 1
        
    all_secret = random.choices(set_secret_prices, k=secret_count)
    secret = [price for price in all_secret if price >= 0.49]
    total += sum(secret)
    
    all_ultra = random.choices(set_ultra_prices, k=ultra_count)
    ultra = [price for price in all_ultra if price >= 0.49]
    total += sum(ultra)
    
    all_super = random.choices(set_super_prices, k=super_count)
    super = [price for price in all_super if price >= 0.49]

    total += sum(super)
    return round(total, 2)

