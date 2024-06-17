# from core.tasks import (get_simulated_total_for_qcr_core_set, 
#                         rarity_collection_get_simulated_booster_total,
#                         rarity_ii_get_simulated_booster_total,
#                         collectors_set_with_qcr_get_booster_total,
#                         collectors_set_without_qcr_get_booster_total,
#                         )
from celery.result import allow_join_result

# def old_simulate_multiple_core_boxes(qcr_core_set_list, num_iterations):
#     results = []
#     chunk_size = 10
#     chunks = [num_iterations // chunk_size for _ in range(chunk_size)]
#     tasks = []
#     # Create and execute Celery tasks for each chunk
#     for chunk in chunks:
#         for _ in range(chunk):
            
#             task = get_simulated_total_for_qcr_core_set.delay(qcr_core_set_list)
#             tasks.append(task)
    
#     # Gather results from Celery tasks
#     with allow_join_result():
#         for task in tasks:
#             print(task.get())
#             results.append(task.get())

#     return results
import random
def new_get_simulated_total_for_qcr_core_set(qcr_core_set_list):
    set_qcr_prices = [card[1] for card in qcr_core_set_list if card[0] == 'Quarter Century']
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
    return total

def simulate_multiple_core_boxes(qcr_core_set_list, num_iterations):
    results = []
    
    for _ in range(num_iterations):
        
        result = new_get_simulated_total_for_qcr_core_set(qcr_core_set_list)
        results.append(result)
    
    return results

def rarity_ii_get_simulated_booster_total(parsed_rarity_ii):
    total = 0
    
    set_qcr_prices = [card[1] for card in parsed_rarity_ii if card[0] == 'Quarter Century']
    set_pcr_prices = [card[1] for card in parsed_rarity_ii if card[0] == "Prismatic Collector's"]
    set_pur_prices = [card[1] for card in parsed_rarity_ii if card[0] == "Prismatic Ultimate"]
    set_ps_prices = [card[1] for card in parsed_rarity_ii if card[0] == "Platinum Secret"]
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

def simulate_multiple_ra02_boxes(parsed_ra02, num_iterations):
    results = []
    
    for _ in range(num_iterations):
        
        result = rarity_ii_get_simulated_booster_total(parsed_ra02)
        results.append(result)
    
    return results

def rarity_collection_get_simulated_booster_total(parsed_rarity_collection):
    total = 0
    
    set_qcr_prices = [card[1] for card in parsed_rarity_collection if card[0] == 'Quarter Century']
    set_pcr_prices = [card[1] for card in parsed_rarity_collection if card[0] == "Prismatic Collector's"]
    set_pur_prices = [card[1] for card in parsed_rarity_collection if card[0] == "Prismatic Ultimate"]
    set_ps_prices = [card[1] for card in parsed_rarity_collection if card[0] == "Platinum Secret"]
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

def simulate_multiple_ra01_boxes(parsed_ra01, num_iterations):
    results = []
    
    for _ in range(num_iterations):
        
        result = rarity_collection_get_simulated_booster_total(parsed_ra01)
        results.append(result)
    
    return results

def collectors_set_with_qcr_get_booster_total(parsed_collector_qcr):
    total = 0

    set_qcr_prices = [card[1] for card in parsed_collector_qcr if card[0] == 'Quarter Century']
    set_collector_prices = [card[1] for card in parsed_collector_qcr if card[0] == "Collector's Rare"]
    set_ultra_prices = [card[1] for card in parsed_collector_qcr if card[0] == "Ultra Rare"]
    set_super_prices = [card[1] for card in parsed_collector_qcr if card[0] == "Super Rare"]

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


def simulate_multiple_collector_qcr_boxes(parsed_collector_qcr, num_iterations):
    results = []
    
    for _ in range(num_iterations):
        
        result = collectors_set_with_qcr_get_booster_total(parsed_collector_qcr)
        results.append(result)
    
    return results

def collectors_set_without_qcr_get_booster_total(parsed_collector):
    total = 0

    set_collector_prices = [card[1] for card in parsed_collector if card[0] == "Collector's Rare"]
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

def simulate_multiple_collector_without_qcr_boxes(parsed_collector, num_iterations):
    results = []
    
    for _ in range(num_iterations):
        
        result = collectors_set_without_qcr_get_booster_total(parsed_collector)
        results.append(result)
    
    return results