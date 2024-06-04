from celery import shared_task
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import random 

@shared_task
def scrape_cards_page(page_url):
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    with webdriver.Chrome(options=chrome_options) as driver:
        driver.get(page_url)
        wait = WebDriverWait(driver, 40)
        try:
            elements = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'search-result')))
            for element in elements:
                wait.until(EC.visibility_of(element))
            print('Page fully loaded')
        except TimeoutException:
            print("Timed out waiting for element to be visible")

        body = driver.find_element(By.TAG_NAME, 'body')
        return body.get_attribute('innerHTML')
    
@shared_task
def scrape_card_detail_page(url):
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    with webdriver.Chrome(options=chrome_options) as driver:
        driver.get(url)
        wait = WebDriverWait(driver, 25)
        try:
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.v-lazy-image.v-lazy-image-loaded')))
            print('page fully loaded')
        except TimeoutException:
            print("Timed out waiting for element to be visible")
        body = driver.find_element(By.TAG_NAME, 'body')
        return body.get_attribute('innerHTML')
    
@shared_task
def get_simulated_total_for_qcr_core_set(qcr_core_set_list):
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

@shared_task
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

@shared_task
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

@shared_task
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
    print(total)
    return total

@shared_task
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
    print(total)
    return total