from core.tasks import (get_simulated_total_for_qcr_core_set, 
                        rarity_collection_get_simulated_booster_total,
                        rarity_ii_get_simulated_booster_total,
                        collectors_set_with_qcr_get_booster_total,
                        collectors_set_without_qcr_get_booster_total,
                        )
from celery.result import allow_join_result

def simulate_multiple_core_boxes(qcr_core_set_list, num_iterations):
    results = []
    chunk_size = 10
    chunks = [num_iterations // chunk_size for _ in range(chunk_size)]
    tasks = []
    # Create and execute Celery tasks for each chunk
    for chunk in chunks:
        for _ in range(chunk):
            
            task = get_simulated_total_for_qcr_core_set.delay(qcr_core_set_list)
            tasks.append(task)
    
    # Gather results from Celery tasks
    with allow_join_result():
        for task in tasks:
            print(task.get())
            results.append(task.get())

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