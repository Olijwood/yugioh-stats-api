from celery import shared_task

import time
import helpers

@shared_task
def scrape_parse_save_cards(url):
    time.sleep(2)  # Optional delay to avoid overloading the server
    sets_cards_data = helpers.main_set_cards(url)
    helpers.cards_save_to_model(sets_cards_data)
    helpers.save_card_prices_to_model(sets_cards_data)
    return

@shared_task
def scrape_parse_save_card_details(url):
    set_cards_details_data = helpers.main_set_cards_details(url)
    helpers.card_details_save_to_model(set_cards_details_data)
    return