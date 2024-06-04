from bs4 import BeautifulSoup
from sets.models import Set
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import time 
from PIL import Image
from io import BytesIO
import os
import requests
from celery.result import allow_join_result

from .utils import last_word
from cards.models import Card
from core.tasks import scrape_cards_page, scrape_card_detail_page

import time

def parse_yugioh_sets(html_soup):
    if not html_soup:
        return []

    sets_data = []

    set_type_mapping = {
        'Booster': 0,
        'Premium Pack': 1,
        'Champion Pack': 2,
        'Tournament Pack': 3,
        'Value Box Pack': 4,
        'Speed Duel': 5,
        'Astral Pack': 6,
        'Turbo Pack': 7,
        'Duelist Pack': 8,
        'Collector Tin': 9,
        'Promo': 10,
        'Reprint / Box Set': 11,
        'Starter Deck': 12,
        'Structure Deck': 13
    }

    sets_div = html_soup.find('div', id='advancedSearchSets')
    sets_uls = sets_div.find_all('ul')

    for set_type, index in set_type_mapping.items():
        sets_a_tags = sets_uls[index].find_all('a')
        sets_data.extend([{'title': a_tag.text, 'link': a_tag.attrs.get('href'), 'type': set_type} for a_tag in sets_a_tags])
    print('parsed sets data')
    return sets_data



def download_image(card_img_src, file_path):
    try:
        # Send a request to get the image URL
        response = requests.get(card_img_src)
        response.raise_for_status()

        # Open the image from the response content
        card_img = Image.open(BytesIO(response.content))

        # Save the image
        with open(file_path, 'wb') as f:
            card_img.save(f, 'JPEG')
        print('Image downloaded successfully!')
    except Exception as e:
        print('Failed to download image:', e)
def old_parse_cards(html_list):
    cards_data = []
    download_path = 'staticfiles-cdn/media/yugioh-card-imgs/'

    if not os.path.exists(download_path):
        os.makedirs(download_path)
    print(len(html_list))
    i = 1
    for page in html_list:
        page_soup = BeautifulSoup(page, 'html.parser')
        search_results = page_soup.find('section', class_='search-results')

        if search_results:
            print(f'found search results for page: {i}')
            card_divs = search_results.find_all('a')

            for card in card_divs:
                card_link = card.attrs.get('href')
                set_name = card.find('h4', class_='product-card__set-name').text
                card_name = card.select_one('span.product-card__title.truncate').text if card.select_one('span.product-card__title.truncate') else None
                rarity_section = card.find('section', class_='product-card__rarity')
                set_name = card.find('h4', class_='product-card__set-name').text
                if rarity_section:
                    card_code = rarity_section.find_all('span')[2].text[1:]
                    card_rarity = '-'.join(rarity_section.find_all('span')[0].text.split()[:2])
                    if card_rarity.split('-')[0] == 'Common':
                        card_rarity = 'Common'
                    if card_code:
                        card_identifier_list = (card_code.split() + [card_rarity])
                        file_name = '-'.join(card_identifier_list) + '.jpg'
                        file_path = os.path.join(download_path, file_name)
                        set_name = card.find('h4', class_='product-card__set-name').text
                        if not os.path.exists(file_path):
                            img_tag = card.find('img')
                            if img_tag:
                                card_img_src = img_tag.get('src')
                                if 'filters:quality(1)/' in card_img_src:
                                        card_img_src = card_img_src.replace('filters:quality(1)/', '')
                                if card_img_src and card_img_src[-4:] == '.jpg' and (set_name != '25th Anniversary Rarity Collection II'):
                                     # Download the image with the best resolution available
                                    download_image(card_img_src, file_path)
                                    print('image downloaded')
                                else:
                                    print('Image not JPG or Image missing')
                            else:
                                print('Image source not found for:', file_name)
                    # print(f'{card.select_one('span.product-card__title.truncate').text}')
                    else:
                        print('no card code')
                elif 'PCR' in card_name and not rarity_section:
                    card_rarity = "Prismatic Collector's"
                if set_name not in card_name:
                    tcg_market_price = None
                    tcg_min_listing = None
                    tcg_num_listings = None
                    
                    try:
                        tcg_market_price_elem = card.select_one('span.product-card__market-price--value')
                        if tcg_market_price_elem:
                            tcg_market_price = float(tcg_market_price_elem.text[1:])
                    except Exception as e:
                        print(f"Error retrieving market price: {e}")

                    try:
                        tcg_min_listing_elem = card.select_one('span.inventory__price-with-shipping')
                        if tcg_min_listing_elem:
                            tcg_min_listing = float(tcg_min_listing_elem.text[1:])
                    except Exception as e:
                        print(f"Error retrieving min listing price: {e}")

                    try:
                        tcg_num_listings_elem = card.select_one('span.inventory__listing-count.inventory__listing-count-block')
                        if tcg_num_listings_elem:
                            tcg_num_listings_text = tcg_num_listings_elem.find('span').text
                            if tcg_num_listings_text:
                                tcg_num_listings = int(tcg_num_listings_text.split()[0])
                    except Exception as e:
                        print(f"Error retrieving number of listings: {e}")
                        
                    card_data = {
                        'card-link': 'https://www.tcgplayer.com' + card_link,
                        'card-name': card.select_one('span.product-card__title.truncate').text if card.select_one('span.product-card__title.truncate') else None,
                        'card-rarity': card_rarity if card_rarity else None,
                        'card-code': card_code if card_code else None,
                        'card-set': card.find('h4').text if card.find('h4') else None,
                        'tcg-market-price': tcg_market_price,
                        'tcg-min-listing': tcg_min_listing,
                        'tcg-num-listings': tcg_num_listings,
                        'card-img-path': file_name,
                    }
                    # print(card_data['card-rarity'])
                    cards_data.append(card_data)
                else:
                    print('no card data, sealed product')
        else:
            print('no search results in set list page')
        i+=1
    print(f'{len(cards_data)} cards in cards data')
    return cards_data

def parse_cards(html_list):
    cards_data = []
    download_path = 'staticfiles-cdn/media/yugioh-card-imgs/'

    if not os.path.exists(download_path):
        os.makedirs(download_path)
    print(len(html_list))
    i = 1
    for page in html_list:
        page_soup = BeautifulSoup(page, 'html.parser')
        search_results = page_soup.find('section', class_='search-results')

        if search_results:
            print(f'found search results for page: {i}')
            card_divs = search_results.find_all('a')

            for card in card_divs:
                card_link = card.attrs.get('href')
                set_name = card.find('h4', class_='product-card__set-name').text
                card_name = card.select_one('span.product-card__title.truncate').text if card.select_one('span.product-card__title.truncate') else None
                rarity_section = card.find('section', class_='product-card__rarity')
                if rarity_section:
                    card_code = rarity_section.find_all('span')[2].text[1:]
                    # print(rarity_section.find_all('span')[0].text)
                    card_rarity = '-'.join(rarity_section.find_all('span')[0].text.split()[:2])
                    if card_rarity.split('-')[0] == 'Common':
                        card_rarity = 'Common'
                    if set_name != '25th Anniversary Rarity Collection II':
                        if card_code:
                            card_identifier_list = (card_code.split() + [card_rarity])
                            file_name = '-'.join(card_identifier_list) + '.jpg'
                            file_path = os.path.join(download_path, file_name)
                            set_name = card.find('h4', class_='product-card__set-name').text
                            if not os.path.exists(file_path):
                                img_tag = card.find('img')
                                if img_tag:
                                    card_img_src = img_tag.get('src')
                                    if 'filters:quality(1)/' in card_img_src:
                                            card_img_src = card_img_src.replace('filters:quality(1)/', '')
                                    if card_img_src and card_img_src[-4:] == '.jpg' and (set_name != '25th Anniversary Rarity Collection II'):
                                         # Download the image with the best resolution available
                                        download_image(card_img_src, file_path)
                                        print('image downloaded')
                                    else:
                                        print('Image not JPG or Image missing')
                                else:
                                    print('Image source not found for:', file_name)
                        # print(f'{card.select_one('span.product-card__title.truncate').text}')
                        else:
                            print('no card code')
                    if set_name == '25th Anniversary Rarity Collection II':
                        file_name = None
                    card_rarity = ' '.join(card_rarity.split('-')) if card_rarity else None
                elif 'PCR' in card_name and not rarity_section:
                    card_rarity = "Prismatic Collector's"
                    card_code = None
                if set_name not in card_name:
                    tcg_market_price = None
                    tcg_min_listing = None
                    tcg_num_listings = None
                    
                    try:
                        tcg_market_price_elem = card.select_one('span.product-card__market-price--value')
                        if tcg_market_price_elem:
                            tcg_market_price = float(tcg_market_price_elem.text[1:])
                    except Exception as e:
                        print(f"Error retrieving market price: {e}")

                    try:
                        tcg_min_listing_elem = card.select_one('span.inventory__price-with-shipping')
                        if tcg_min_listing_elem:
                            tcg_min_listing = float(tcg_min_listing_elem.text[1:])
                    except Exception as e:
                        print(f"Error retrieving min listing price: {e}")

                    try:
                        tcg_num_listings_elem = card.select_one('span.inventory__listing-count.inventory__listing-count-block')
                        if tcg_num_listings_elem:
                            tcg_num_listings_text = tcg_num_listings_elem.find('span').text
                            if tcg_num_listings_text:
                                tcg_num_listings = int(tcg_num_listings_text.split()[0])
                    except Exception as e:
                        print(f"Error retrieving number of listings: {e}")
                        
                    card_data = {
                        'card-link': 'https://www.tcgplayer.com' + card_link,
                        'card-name': card.select_one('span.product-card__title.truncate').text if card.select_one('span.product-card__title.truncate') else None,
                        'card-rarity': card_rarity if card_rarity else None,
                        'card-code': card_code if card_code else None,
                        'card-set': card.find('h4').text if card.find('h4') else None,
                        'tcg-market-price': tcg_market_price,
                        'tcg-min-listing': tcg_min_listing,
                        'tcg-num-listings': tcg_num_listings,
                        'card-img-path': file_name if file_name else None,
                    }
                    # print(card_data['card-rarity'])
                    cards_data.append(card_data)
                else:
                    print('no card data, sealed product')
        else:
            print('no search results in set list page')
        i+=1
    print(f'{len(cards_data)} cards in cards data')
    return cards_data



def main_set_cards(url):
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    url = str(url)
    print(url)

    with webdriver.Chrome(options=chrome_options) as driver:
        driver.get(url)
        wait = WebDriverWait(driver, 25)
        
        try:
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.search-layout__pagination')))
            print('Page fully loaded')
        except TimeoutException:
            print("Timed out waiting for element to be visible")
        
        try:
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.tcg-pagination__pages')))
            print('pagination pages found')
        except TimeoutException:
            print('Timed out waiting for element')
        pagination_div = driver.find_element(By.CSS_SELECTOR, 'div.tcg-pagination__pages')
        pagination_a_tags = pagination_div.find_elements(By.TAG_NAME, 'a')
        pagination_links = [x.get_attribute('href') for x in pagination_a_tags]

        
        print(pagination_links)

        

    # List to store the task results
    task_results = []
    # Get the base URL without the page number
    # set_url_no_page = 'https://www.tcgplayer.com' + '='.join(pagination_links[0].split('=')[:-1]) + '='
    set_url_no_page = pagination_links[0].split('page=')[0] + 'page='
    # Extract the last page number from the last URL
    last_page_num = int(pagination_links[-1].split('page=')[1].split('&')[0])

    # Generate the list of all page URLs
    page_urls = [f"{set_url_no_page}{page_num}" for page_num in range(1, last_page_num + 1)]

    print(page_urls)
    # Asynchronously call scrape_cards_page for each page URL
    for page_url in page_urls:
        # page_url = 'https://www.tcgplayer.com' + raw_page_url
        task = scrape_cards_page.delay(page_url)
        task_results.append(task)
    # Wait for all tasks to complete and retrieve their results
    with allow_join_result():
        html_list = [task_result.get() for task_result in task_results]
   
    print(len(html_list))
    cards_data = parse_cards(html_list)
    return cards_data

def parse_card_details(html_list, url_list):
    cards_detail_data = []

    for card_html, url in zip(html_list, url_list):
        soup = BeautifulSoup(card_html, 'html.parser')
        card_name = soup.find('h1', class_='product-details__name').text
        card_information = soup.find('section', class_='product-details__details')
        card_lore = card_information.find('div', class_='product__item-details__description').text
        card_types_list = card_information.find('ul', class_='product__item-details__attributes')
        card_types = card_types_list.find_all('span')[2].text
        card_type = card_types.split('/')[-1]
        parse_card_type = (last_word(card_type)).strip()
        if 'Token' in card_type:
            parse_card_type = 'Token'

        attribute = None
        archtype = None
        level = None
        atk = None
        def_ = None
        
        print(f'PrseTyp: {parse_card_type} - {card_name}')
        if parse_card_type == 'Monster':
            attribute = (card_types.split('/')[0]).split()[0]
            archtype = ' '.join(card_types.split('/')[0].split()[1:])
            if card_types.split('/')[1] == 'Xyz':
                card_type = card_type.split()[0] + ' Xyz ' + card_type.split()[1]
            elif card_types.split('/')[1] == 'Link':
                card_type = card_type.split()[0] + ' Link ' + card_type.split()[1]
            elif card_types.split('/')[1] == 'Synchro':
                card_type = card_type.split()[0] + ' Synchro ' + card_type.split()[1]
            elif card_types.split('/')[1] == 'Pendulum':
                card_type = card_type.split()[0] + ' Pendulum ' + card_type.split()[1]
            if 'Link' in str(card_type):
                atk_raw = card_types_list.find_all('span')[3].text
                atk = str(atk_raw[:-3])
                def_ = None
                level = card_types_list.find_all('span')[4].text
            elif 'Xyz' in str(card_type):
                try: 
                    atk_def = card_types_list.find_all('span')[3].text
                    atk = str(atk_def.split(' / ')[0]).strip()
                    def_ = str(atk_def.split(' /')[1]).strip()
                    level = None
                except: 
                    atk_def = card_types_list.find_all('span')[4].text
                    atk = str(atk_def.split(' / ')[0]).strip()
                    def_ = str(atk_def.split(' /')[1]).strip()
            elif 'Pendulum' in str(card_type):
                atk_def = card_types_list.find_all('span')[4].text
                atk = str(atk_def.split(' / ')[0]).strip()
                def_ = str(atk_def.split(' /')[1]).strip()
                level = card_types_list.find_all('span')[3].text
            else:
                atk_def = card_types_list.find_all('span')[4].text
                atk = str(atk_def.split(' / ')[0]).strip()
                def_ = str(atk_def.split(' /')[1]).strip()
                level = card_types_list.find_all('span')[3].text
                
        elif parse_card_type == 'Spell' or parse_card_type == 'Trap':
            attribute = (card_types.split('/')[0]).strip()
            archtype = None
            level = None
            atk = None
            def_ = None

        elif parse_card_type == 'Token':
            attribute = None
            archtype = None
            level = None
            atk = None
            def_ = None
            
        cards_detail_data.append({
            'card_name': card_name,
            'card_id': Card.objects.values_list('id', flat=True).get(card_link = url),
            'lore': card_lore,
            'type': card_type,
            'simple_type': parse_card_type,
            'attribute': attribute,
            'archtype': archtype,
            'level': level,
            'atk': atk,
            'def': def_
        })
    return cards_detail_data

def main_set_cards_details(set_url):
    html_list = []
    chunk_size = 8

    set_card_links = Card.objects.values_list('card_link', flat=True).filter(set__link=str(set_url))
    url_chunks = [set_card_links[i:i + chunk_size] for i in range(0, len(set_card_links), chunk_size)]


    for url_chunk in url_chunks:
        tasks = []
        for url in url_chunk:
            time.sleep(0.5)
            task = scrape_card_detail_page.delay(url)
            tasks.append(task)
        with allow_join_result():
            for task_result in tasks:
                html_list.append(task_result.get())
        print('scraped urls in chunk')
    print(len(html_list))
    cards_detail_data = parse_card_details(html_list, set_card_links)
    return cards_detail_data

