from celery import shared_task
from celery.result import allow_join_result
from datetime import date
import os
import pandas as pd

import helpers

from .models import Set, SetSimulatedPriceStats
from cards.models import Card
from cards.tasks import scrape_parse_save_cards, scrape_parse_save_card_details

@shared_task
def scrape_parse_save_yugioh_sets():
    url = 'https://shop.tcgplayer.com/yugioh?newSearch=true&_gl=1*sgexa9*_gcl_au*MzcyOTUwOTU3LjE3MTA5MjM5MzA.*_ga*MTk3NTI4NjUyMy4xNzEwOTIzOTMw*_ga_VS9BE2Z3GY*MTcxMzM0MzE2MC40Mi4wLjE3MTMzNDMxNjAuNjAuMC4w'
    html_soup = helpers.scrape_yugioh_sets(url)
    sets_data = helpers.parse_yugioh_sets(html_soup)
    helpers.sets_save_to_model(sets_data)
    return

@shared_task
def main_scrape_cards_and_details():
    string_codes_for_cllcrt_sets = ['WISU', 'MAZE', 'AMDE', 'TAMA', 'GRCR', 'KICO', 'ANGU', 'GEIM', 'TOCH'] # no QCR
    set_links = Set.objects.values_list('link', flat=True)
    cllctr_sets = [Set.objects.get(code=set_code) for set_code in string_codes_for_cllcrt_sets]
    # test_set_links = [cllctr_set.link for cllctr_set in cllctr_sets]
    sets_with_code = Set.objects.exclude(code = None)
    test_set_links = list(sets_with_code.values_list('link', flat = True))
    # test_set_links = list(set_links[1:4]) + [set_links[7]] + [set_links[9]] # Ones with stats
    # test_set_links = list(set_links[1:6]) + list(set_links[7:10]) # First 10
    # test_set_links = [set_links[11]] + [set_links[13]] + [set_links[14]] # First 3 Collector Rare
    # test_set_links = list(set_links[1:6]) + [set_links[7]] + list(set_links[9:10]) + list(set_links[11:16]) + list(set_links[17:19])
    chunk_size = 2
    url_chunks = [test_set_links[i:i + chunk_size] for i in range(0, len(test_set_links), chunk_size)]

    for url_chunk in url_chunks:
        cards_tasks = []
        for url in url_chunk:
            cards_task = scrape_parse_save_cards.delay(url)
            cards_tasks.append(cards_task)
        with allow_join_result():
            completed = [task_result.get() for task_result in cards_tasks]

        # details_tasks = []
        # for url in url_chunk:
        #     set_name = Set.objects.values_list('title', flat=True).filter(link=str(url)).first()
        #     set_last_card = Card.objects.filter(set__link = str(url)).values_list('lore', flat=True).last()
        #     if set_last_card == None:
        #         print(f'No Card Details for {set_name}')
        #         details_task = scrape_parse_save_card_details.delay(url)
        #         details_tasks.append(details_task)
        #     else:
        #         print(f'Already have Card Details for {set_name}')
        # if details_tasks:
        #     with allow_join_result():
        #         completed = [task_result.get() for task_result in details_tasks]

@shared_task
def simulated_qcr_core_sets_booster_stats():
    qcr_core_set_code_strings = ['PHNI', 'AGOV', 'DUNE', 'LEDE']
    num_iterations = 100000
    sets_booster_stats_data = []
    for qcr_core_set_string in qcr_core_set_code_strings:
        qcr_core_set = Set.objects.get(code=qcr_core_set_string)
        cards_qcr_core_set = Card.objects.filter(set=qcr_core_set)
        set_booster_price = qcr_core_set.average_price
        
        mp_parsed_qcr_core_set = [[card.card_rarity, card.get_market_price()] for card in cards_qcr_core_set if card.get_market_price() != None]
        mp_simulated_values = helpers.simulate_multiple_core_boxes(mp_parsed_qcr_core_set, num_iterations)
        helpers.save_results_to_csv(qcr_core_set_string, mp_simulated_values, 'MP')

        mp_set_booster_stats_data = helpers.get_stats_for_simulated_set(qcr_core_set_string, 'MP', set_booster_price)

        ml_parsed_qcr_core_set = [[card.card_rarity, card.get_min_listing()] for card in cards_qcr_core_set if card.get_min_listing() != None]
        ml_simulated_values = helpers.simulate_multiple_core_boxes(ml_parsed_qcr_core_set, num_iterations)
        helpers.save_results_to_csv(qcr_core_set_string, ml_simulated_values, 'ML')
        ml_set_booster_stats_data = helpers.get_stats_for_simulated_set(qcr_core_set_string, 'ML', set_booster_price)
       
        sets_booster_stats_data.append({
            'set_link': qcr_core_set.link,
            'simulated_market_p_stats': mp_set_booster_stats_data,
            'simulated_min_listing_stats': ml_set_booster_stats_data
        })
        print(sets_booster_stats_data)
        print(f'Successfully simulated {qcr_core_set_string} ')
    helpers.set_stats_save_to_model(sets_stats_data=sets_booster_stats_data)
    print('Saved qcr core sets to model')
    return

@shared_task
def simulated_rarity_ii_booster_stats():
    ra02 = Set.objects.filter(link = 'https://www.tcgplayer.com/search/yugioh/25th-anniversary-rarity-collection-ii').first()
    ra02_cards = Card.objects.filter(set=ra02)
    num_iterations = 100000
    sets_booster_stats_data = []
    set_booster_price = ra02.average_price
    set_code = ra02.code
    ml_parsed_ra02 = [[card.card_rarity, card.get_min_listing()] for card in ra02_cards if card.get_min_listing() != None]
    ml_simulated_values = helpers.simulate_multiple_ra02_boxes(ml_parsed_ra02, num_iterations)
    helpers.save_results_to_csv(set_code, ml_simulated_values, 'ML')
    ml_set_booster_stats_data = helpers.get_stats_for_simulated_set(set_code, 'ML',set_booster_price)
    
    mp_parsed_ra02 = [[card.card_rarity, card.get_market_price()] for card in ra02_cards if card.get_market_price() != None]
    mp_simulated_values = helpers.simulate_multiple_ra02_boxes(mp_parsed_ra02, num_iterations)
    helpers.save_results_to_csv(set_code, mp_simulated_values, 'MP')
    mp_set_booster_stats_data = helpers.get_stats_for_simulated_set(set_code, 'MP', set_booster_price)
    
    
    sets_booster_stats_data.append({
        'set_link': str(ra02.link),
        'simulated_market_p_stats': mp_set_booster_stats_data,
        'simulated_min_listing_stats': ml_set_booster_stats_data
    })
    print(f'Successfully simulated: Rarity Collection II - ({num_iterations} times)')
    helpers.set_stats_save_to_model(sets_stats_data=sets_booster_stats_data)
    print('Saved Ra02 Stats to model')
    return

@shared_task
def simulated_rarity_collection_booster_stats():
    num_iterations = 100000
    sets_booster_stats_data = []

    ra01 = Set.objects.get(code='RA01')
    ra01_cards = Card.objects.filter(set=ra01)

    set_booster_price = ra01.average_price
    set_code = ra01.code

    mp_parsed_ra01 = [[card.card_rarity, card.get_market_price()] for card in ra01_cards if card.get_market_price() != None]
    mp_simulated_values = helpers.simulate_multiple_ra01_boxes(mp_parsed_ra01, num_iterations)
    helpers.save_results_to_csv(set_code=set_code,
                                                 results=mp_simulated_values,
                                                 MPorML='MP')
    mp_set_booster_stats_data = helpers.get_stats_for_simulated_set(set_code, 'MP', set_booster_price)

    ml_parsed_ra01 = [[card.card_rarity, card.get_min_listing()] for card in ra01_cards if card.get_min_listing() != None]
    ml_simulated_values = helpers.simulate_multiple_ra01_boxes(ml_parsed_ra01, num_iterations)
    helpers.save_results_to_csv(set_code=set_code,
                                                results=ml_simulated_values,
                                                MPorML='ML')
    ml_set_booster_stats_data = helpers.get_stats_for_simulated_set(set_code, 'ML', set_booster_price)
    sets_booster_stats_data.append({
        'set_link': str(ra01.link),
        'simulated_market_p_stats': mp_set_booster_stats_data,
        'simulated_min_listing_stats': ml_set_booster_stats_data,

    })
    print(f'Successfully simulated: Rarity Collection 1 - ({num_iterations} times)')
    helpers.set_stats_save_to_model(sets_stats_data=sets_booster_stats_data)
    print('Saved Rarity Collection Stats to model')
    return



@shared_task
def simulated_collector_without_qcr_booster_stats():
    string_codes_for_cllcrt_sets = ['WISU', 'MAZE', 'AMDE', 'TAMA', 'GRCR', 'KICO', 'ANGU', 'GEIM', 'TOCH'] # no QCR
    sets_booster_stats_data = []
    num_iterations = 100000

    for cllctr_set_code in string_codes_for_cllcrt_sets:
        cllctr_set = Set.objects.get(code=cllctr_set_code)
        booster_price = cllctr_set.average_price
        cllctr_set_cards = Card.objects.filter(set=cllctr_set)
        
        mp_parsed_cllctr_set_cards = [[card.card_rarity, card.get_market_price()] for card in cllctr_set_cards if card.get_market_price() != None]
        mp_simulated_totals = helpers.simulate_multiple_collector_without_qcr_boxes(
                            mp_parsed_cllctr_set_cards, 
                            num_iterations)
        helpers.save_results_to_csv(cllctr_set_code, mp_simulated_totals, 'MP')
        mp_set_booster_stats_data = helpers.get_stats_for_simulated_set(
            cllctr_set_code, 'MP', booster_price 
        )

        ml_parsed_cllctr_set_cards = [[card.card_rarity, card.get_min_listing()] for card in cllctr_set_cards if card.get_min_listing() != None]
        ml_simulated_totals = helpers.simulate_multiple_collector_without_qcr_boxes(
                            ml_parsed_cllctr_set_cards, 
                            num_iterations)
        helpers.save_results_to_csv(cllctr_set_code, ml_simulated_totals, 'ML')
        ml_set_booster_stats_data = helpers.get_stats_for_simulated_set(
            cllctr_set_code, 'ML', booster_price 
        )

        sets_booster_stats_data.append({
            'set_link': cllctr_set.link,
            'simulated_market_p_stats': mp_set_booster_stats_data,
            'simulated_min_listing_stats': ml_set_booster_stats_data,
        })
        print(f'Successfully simulated {cllctr_set.code} ({num_iterations} times)')
    helpers.set_stats_save_to_model(sets_booster_stats_data)
    print('Saved collector sets to model')
    return

@shared_task
def simulated_collector_with_qcr_booster_stats():
    code_strings_for_collector_sets_with_qcr = ['VASM', 'MZMI']
    sets_booster_stats_data = []
    num_iterations = 100000

    for cllctr_set_code in code_strings_for_collector_sets_with_qcr:
        cllctr_set = Set.objects.get(code=cllctr_set_code)
        booster_price = cllctr_set.average_price
        cllctr_set_cards = Card.objects.filter(set=cllctr_set)
        
        mp_parsed_cllctr_set_cards = [[card.card_rarity, card.get_market_price()] for card in cllctr_set_cards if card.get_market_price() != None]
        mp_simulated_totals = helpers.simulate_multiple_collector_qcr_boxes(
                            mp_parsed_cllctr_set_cards, 
                            num_iterations)
        helpers.save_results_to_csv(cllctr_set_code, mp_simulated_totals, 'MP')
        mp_set_booster_stats_data = helpers.get_stats_for_simulated_set(
            cllctr_set_code, 'MP', booster_price 
        )

        ml_parsed_cllctr_set_cards = [[card.card_rarity, card.get_min_listing()] for card in cllctr_set_cards if card.get_min_listing() != None]
        ml_simulated_totals = helpers.simulate_multiple_collector_qcr_boxes(
                            ml_parsed_cllctr_set_cards, 
                            num_iterations)
        helpers.save_results_to_csv(cllctr_set_code, ml_simulated_totals, 'ML')
        ml_set_booster_stats_data = helpers.get_stats_for_simulated_set(
            cllctr_set_code, 'ML', booster_price 
        )

        sets_booster_stats_data.append({
            'set_link': cllctr_set.link,
            'simulated_market_p_stats': mp_set_booster_stats_data,
            'simulated_min_listing_stats': ml_set_booster_stats_data,
        })
        print(f'Successfully simulated {cllctr_set.code} ({num_iterations} times)')
    helpers.set_stats_save_to_model(sets_booster_stats_data)
    print('Saved collector qcr sets to model')
    return

@shared_task
def update_set_gainloss():
    today = date.today()
    set_codes = list(SetSimulatedPriceStats.objects.values_list('set__code', flat=True).distinct())
    for set_code in set_codes:
        set_data_directory = helpers.get_set_data_directory(set_code)
        set_instance = Set.objects.get(code=set_code)
        booster_price = float(set_instance.average_price)
        
        ml_filepath = os.path.join(set_data_directory, f'ml{set_code}.csv')
        mp_filepath = os.path.join(set_data_directory, f'mp{set_code}.csv')
        
        ml_df = pd.read_csv(ml_filepath)
        mp_df = pd.read_csv(mp_filepath)
        
        ml_len = len(ml_df['Total'])
        mp_len = len(mp_df['Total'])
        
        mp_difference = sum(mp_df['Total']) - (booster_price*mp_len)
        mp_gainloss = round((mp_difference/mp_len), 2)
        ml_difference = sum(ml_df['Total']) - (booster_price*ml_len)
        ml_gainloss = round((ml_difference/ml_len), 2)
        
        today_setstats_instance = SetSimulatedPriceStats.objects.filter(set=set_instance).filter(date_simulated=today).last()
        today_setstats_instance.booster_gainloss_mp = mp_gainloss
        today_setstats_instance.booster_gainloss_ml = ml_gainloss
        today_setstats_instance.save()

@shared_task
def update_graphs_for_sets():
    set_codes = helpers.get_valid_set_codes()
    for set_code in set_codes:
        success = helpers.create_update_set_graphs(set_code)
        if success != 1:
            print(f'Error Updating Graphs for {set_code}')
    print('Finished updating graphs for Yugioh Sets')
    helpers.create_update_sets_gl_graphs()

@shared_task
def save_sets_cgv_rankings():
    ml_rankings = helpers.save_ml_rankings()
    print(ml_rankings)
    mp_rankings = helpers.save_mp_rankings()
    print(mp_rankings)
    helpers.update_ranking_change()
    return

@shared_task
def save_sets_gainloss_rankings():
    helpers.save_gainloss_rankings_ml()
    helpers.save_gainloss_rankings_mp()
    helpers.update_gl_ranking_change()
    return

