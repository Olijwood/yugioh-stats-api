from core.tasks import (get_simulated_total_for_qcr_core_set, 
                        rarity_collection_get_simulated_booster_total,
                        rarity_ii_get_simulated_booster_total,
                        collectors_set_with_qcr_get_booster_total,
                        collectors_set_without_qcr_get_booster_total,
                        )
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

def simulate_multiple_ra02_boxes(parsed_ra02, num_iterations):
    results = []
    chunk_size = 10
    chunks = [num_iterations // chunk_size for _ in range(chunk_size)]
    tasks = []
    # Create and execute Celery tasks for each chunk
    for chunk in chunks:
        for _ in range(chunk):
            
            task = rarity_ii_get_simulated_booster_total.delay(parsed_ra02)
            tasks.append(task)
    
    # Gather results from Celery tasks
    with allow_join_result():
        for task in tasks:
            print(task.get())
            results.append(task.get())

    return results

def simulate_multiple_ra01_boxes(parsed_ra01, num_iterations):
    results = []
    chunk_size = 10
    chunks = [num_iterations // chunk_size for _ in range(chunk_size)]
    tasks = []
    # Create and execute Celery tasks for each chunk
    for chunk in chunks:
        for _ in range(chunk):
            
            task = rarity_collection_get_simulated_booster_total.delay(parsed_ra01)
            tasks.append(task)
    
    # Gather results from Celery tasks
    with allow_join_result():
        for task in tasks:
            print(task.get())
            results.append(task.get())

    return results


def simulate_multiple_collector_qcr_boxes(parsed_collector_qcr, num_iterations):
    results = []
    chunk_size = 10
    chunks = [num_iterations // chunk_size for _ in range(chunk_size)]
    tasks = []
    # Create and execute Celery tasks for each chunk
    for chunk in chunks:
        for _ in range(chunk):
            
            task = collectors_set_with_qcr_get_booster_total.delay(parsed_collector_qcr)
            tasks.append(task)
    
    # Gather results from Celery tasks
    with allow_join_result():
        for task in tasks:
            print(task.get())
            results.append(task.get())

    return results

def simulate_multiple_collector_without_qcr_boxes(parsed_collector, num_iterations):
    results = []
    chunk_size = 10
    chunks = [num_iterations // chunk_size for _ in range(chunk_size)]
    tasks = []
    # Create and execute Celery tasks for each chunk
    for chunk in chunks:
        for _ in range(chunk):
            
            task = collectors_set_without_qcr_get_booster_total.delay(parsed_collector)
            tasks.append(task)
    
    # Gather results from Celery tasks
    with allow_join_result():
        for task in tasks:
            print(task.get())
            results.append(task.get())

    return results