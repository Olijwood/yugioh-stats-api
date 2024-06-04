from django.utils import timezone
from sets.models import Set, SetScrapeRecord, SetSimulatedPriceStats, SetRankings, SetGainLossRanking
from cards.models import Card, CardImage, PriceHistory
from datetime import date, timedelta
from dateutil import relativedelta
from .utils import get_valid_set_codes
import os

def sets_save_to_model(sets_data):
    current_time = timezone.now()
    created_updated = False
    for x in sets_data:
        set_obj, created = Set.objects.update_or_create(
            link=x.get('link'),
            defaults={
                'title': x.get('title'),
                'type': x.get('type'),
                'updated': current_time
            }
        )

        if created:
            print(f"Set '{set_obj.title}' created.")
            created_updated = True
        elif (set_obj.title != x.get('title') or set_obj.type != x.get('type')):
            set_obj.title = x.get('title')
            set_obj.type = x.get('type')
            set_obj.updated = current_time
            set_obj.save()
            print(f"Set '{set_obj.title}' updated.")
            created_updated = True
    if created_updated:
        print('Sets updated / created')
    else:
        print('Up to date! No sets created or updated')
    SetScrapeRecord.objects.create(
        timestamp = current_time
    )

def cards_save_to_model(cards_data):
    cards_to_update = []

    for x in cards_data:
        set_title = x.get('card-set')
        set_obj = Set.objects.get(title=set_title)
        try:
            card_obj = Card.objects.get(card_link=x.get('card-link'))
            print(card_obj)
             # Check if any of the fields have changed
            if (
                card_obj.tcg_num_listings != x.get('tcg-num-listings') or
                card_obj.card_rarity != x.get('card-rarity') or
                card_obj.card_code != x.get('card-code') or
                card_obj.card_name != x.get('card-name')
               ):

                cards_to_update.append(Card(
                    id=card_obj.id,
                    card_name=x.get('card-name'),
                    tcg_num_listings=x.get('tcg-num-listings'),
                    card_rarity=x.get('card-rarity'),
                    card_code=x.get('card-code')
                ))
            try:
                card_image_obj = CardImage.objects.get(card=card_obj)
            except CardImage.DoesNotExist:
                # Create or update CardImage
                file_name = x.get('card-img-path')
                if file_name is not None:
                    file_path = os.path.join('staticfiles-cdn/media/yugioh-card-imgs', file_name)
                    if os.path.exists(file_path):
                        card_image_obj, created = CardImage.objects.get_or_create(card=card_obj)
                        card_image_obj.image_path = file_path
                        card_image_obj.save()
                        print(f"Image for Card '{card_obj}' saved.")
                    else:
                        print(f"Image file '{file_name}' does not exist.")
        except Card.DoesNotExist:
            try:
                card_obj = Card.objects.create(
                    set=set_obj,
                    card_name=x.get('card-name'),
                    card_link=x.get('card-link'),
                    card_code=x.get('card-code'),
                    card_rarity=x.get('card-rarity'),
                    tcg_num_listings=x.get('tcg-num-listings')
                )
                # print(f"Card '{card_obj}' created.")
            # Create or update CardImage
                file_name = x.get('card-img-path')
                if file_name is not None:
                    file_path = os.path.join('staticfiles-cdn/media/yugioh-card-imgs', file_name)
                    if os.path.exists(file_path):
                        card_image_obj, created = CardImage.objects.get_or_create(card=card_obj)
                        card_image_obj.image_path = file_path
                        card_image_obj.save()
                        print(f"Image for Card '{card_obj}' saved.")
                    else:
                        print(f"Image file '{file_name}' does not exist.")
            except:
                print(f'{x.get('card-name')}-{x.get('card-rarity')} not created')
    if cards_to_update:
        Card.objects.bulk_update(cards_to_update, ['tcg_num_listings', 'card_rarity', 'card_code'])
        print(f'cards data for {set_title} updated')
    
    print('All cards data saved to model.')

def save_card_prices_to_model(cards_data):
    for card_data in cards_data:
        card_link = card_data.get('card-link')
        tcg_market_price = card_data.get('tcg-market-price')
        tcg_min_listing = card_data.get('tcg-min-listing')
        
        try:
            card = Card.objects.get(card_link=card_link)
            price_history = PriceHistory.objects.create(
                card=card,
                tcg_market_price=tcg_market_price,
                tcg_min_listing=tcg_min_listing,
                date=date.today()
            )
            print(f"Price history for '{card}' saved.")
        except Card.DoesNotExist:
            print(f"Card with link '{card_link}' does not exist.")

    print('All card prices data saved to PriceHistory.')

def card_details_save_to_model(card_details_data):
    cards_to_update = []

    for x in card_details_data:
        try:
            card = Card.objects.get(id=x.get('card_id'))
        except Card.DoesNotExist:
            print('No card saved with ID provided')
            continue

        if (card.lore != x.get('lore') or
                card.card_type != x.get('type') or
                card.simple_type != x.get('simple_type') or
                card.attribute != x.get('attribute') or
                card.archtype != x.get('archtype') or
                card.level != x.get('level') or
                card.card_atk != x.get('atk') or
                card.card_def != x.get('def')):

            card.lore = x.get('lore')
            card.card_type = x.get('type')
            card.simple_type = x.get('simple_type')
            card.attribute = x.get('attribute')
            card.archtype = x.get('archtype')
            card.level = x.get('level')
            card.card_atk = x.get('atk')
            card.card_def = x.get('def')
            cards_to_update.append(card)

    if cards_to_update:
        Card.objects.bulk_update(cards_to_update, fields=[
            'lore', 'card_type', 'simple_type', 'attribute',
            'archtype', 'level', 'card_atk', 'card_def'
        ])
        print('All cards details saved or updated!')
    else:
        print('No card details to update.')

def set_stats_save_to_model(sets_stats_data):
    for set_stats in sets_stats_data:
        print(set_stats)
        set_link = set_stats['set_link']
        set_obj = Set.objects.get(link=set_link)
        mp_set_stats_data = set_stats['simulated_market_p_stats']
        ml_set_stats_data = set_stats['simulated_min_listing_stats']
        
        SetSimulatedPriceStats.objects.create(
            set = set_obj,
            booster_mean_marketp = mp_set_stats_data['mean_value'],
            booster_median_marketp = mp_set_stats_data['median_value'],
            chance_greater_opened_value_marketp = mp_set_stats_data['chance_higher_value'],

            booster_mean_minlisting = ml_set_stats_data['mean_value'],
            booster_median_minlisting = ml_set_stats_data['median_value'],
            chance_greater_opened_value_minlisting = ml_set_stats_data['chance_higher_value'],
            
            date_simulated = mp_set_stats_data['date_updated']
        )
        print(f'Saved simulated price stats for {set_obj.title}')

# Function to calculate percentage change
def calculate_change(today_value, past_value):
    if past_value is not None:
        change = today_value - past_value
        change_percent = round((change / past_value) * 100, 2) if past_value != 0 else float(0)
        return change_percent
    else:
        return None
        
def save_mp_rankings():
    today = date.today()
    seven_days_ago = today - timedelta(days=7)
    one_month_ago = today - relativedelta.relativedelta(months=1)
    set_stats_today = SetSimulatedPriceStats.objects.filter(date_simulated=today).order_by('-chance_greater_opened_value_marketp')    

    set_stats_seven_days_ago = SetSimulatedPriceStats.objects.filter(date_simulated=seven_days_ago)
    set_stats_one_month_ago = SetSimulatedPriceStats.objects.filter(date_simulated=one_month_ago)

    # Create dictionaries for quick lookup of the stats by set code
    stats_seven_days_ago_dict = {stat.set.code: stat.chance_greater_opened_value_marketp for stat in set_stats_seven_days_ago}
    stats_one_month_ago_dict = {stat.set.code: stat.chance_greater_opened_value_marketp for stat in set_stats_one_month_ago}
    
    ranking = 1

    for set_today in set_stats_today:
        set_code = set_today.set.code
        today_chance = round(set_today.chance_greater_opened_value_marketp, 2)
        # Calculate the 7-day change
        chance_seven_days_ago = stats_seven_days_ago_dict.get(set_code)
        seven_change_percent = calculate_change(today_chance, chance_seven_days_ago)

        # Calculate the 1-month change
        chance_one_month_ago = stats_one_month_ago_dict.get(set_code)
        one_month_change_percent = calculate_change(today_chance, chance_one_month_ago)

        # Calculate the all-time change
        first_set_cgvmp = SetSimulatedPriceStats.objects.filter(set__code=set_code).order_by('date_simulated').first().chance_greater_opened_value_marketp
        all_time_cvgmp_change_percent = calculate_change(today_chance, first_set_cgvmp)

        # Save the data to the SetRankings model
        SetRankings.objects.update_or_create(
            set=set_today.set,
            ranking_date=date.today(),
            defaults={
                'mp_ranking': ranking,
                'mp_cgv_today': today_chance,
                'mp_cgv_week': seven_change_percent,
                'mp_cgv_month': one_month_change_percent,
                'mp_cgv_all_time': all_time_cvgmp_change_percent,
            }
        )
        ranking += 1

    return "MP Rankings saved successfully."


def save_ml_rankings():
    today = date.today()
    seven_days_ago = today - timedelta(days=7)
    one_month_ago = today - relativedelta.relativedelta(months=1)

    set_stats_today = SetSimulatedPriceStats.objects.filter(date_simulated=date.today()).order_by('-chance_greater_opened_value_minlisting')    
    # Retrieve stats from 7 days ago and 1 month ago
    set_stats_seven_days_ago = SetSimulatedPriceStats.objects.filter(date_simulated=seven_days_ago)
    set_stats_one_month_ago = SetSimulatedPriceStats.objects.filter(date_simulated=one_month_ago)

    # Create dictionaries for quick lookup of the stats by set code
    stats_seven_days_ago_dict = {stat.set.code: stat.chance_greater_opened_value_minlisting for stat in set_stats_seven_days_ago}
    stats_one_month_ago_dict = {stat.set.code: stat.chance_greater_opened_value_minlisting for stat in set_stats_one_month_ago}


    ranking = 1

    for set_today in set_stats_today:
        set_code = set_today.set.code
        mp_today_chance = set_today.chance_greater_opened_value_marketp
        today_chance = round(set_today.chance_greater_opened_value_minlisting, 2)
        
        # Calculate the 7-day change
        chance_seven_days_ago = stats_seven_days_ago_dict.get(set_code)
        seven_change_percent = calculate_change(today_chance, chance_seven_days_ago)

        # Calculate the 1-month change
        chance_one_month_ago = stats_one_month_ago_dict.get(set_code)
        one_month_change_percent = calculate_change(today_chance, chance_one_month_ago)

        # Calculate the all-time change
        set_list_ml_cgv = list(SetSimulatedPriceStats.objects.values_list('chance_greater_opened_value_minlisting', flat=True).filter(set__code=set_code))
        first_ml_cgv = [ml_cgv for ml_cgv in set_list_ml_cgv if ml_cgv != None][0]
        all_time_cvgml_change_percent = calculate_change(today_chance, first_ml_cgv)

        SetRankings.objects.update_or_create(
            set=set_today.set,
            ranking_date=date.today(),
            defaults={
                'ml_ranking': ranking,
                'mp_cgv_today': mp_today_chance,
                'ml_cgv_today': today_chance,
                'ml_cgv_week': seven_change_percent,
                'ml_cgv_month': one_month_change_percent,
                'ml_cgv_all_time': all_time_cvgml_change_percent,
            }
        )
        ranking += 1

    return "ML Rankings saved successfully."

def save_gainloss_rankings_mp():
    
    today = date.today()
    seven_days_ago = date.today() - timedelta(days=7)
    one_month_ago = date.today() - relativedelta.relativedelta(months=1)
    # {'RA02': set_gainloss_mp
    # set_gainloss_mp = {}
    stats_today = SetSimulatedPriceStats.objects.filter(date_simulated=today).order_by('-booster_gainloss_mp')
    stats_7d_ago = SetSimulatedPriceStats.objects.filter(date_simulated=seven_days_ago)
    stats_1m_ago = SetSimulatedPriceStats.objects.filter(date_simulated=one_month_ago)

    dict_stats_7d_ago = {stat.set.code: stat.booster_gainloss_mp for stat in stats_7d_ago}
    dict_stats_1m_ago = {stat.set.code: stat.booster_gainloss_mp for stat in stats_1m_ago}
    ranking = 1
    for stat_today in stats_today:
        set_code = stat_today.set.code
        today_mp_gainloss = SetSimulatedPriceStats.objects.filter(set__code=set_code).filter(date_simulated=today).last().booster_gainloss_mp
        d7_mp_gainloss = dict_stats_7d_ago.get(set_code)
        d7_change_p = calculate_change(today_mp_gainloss, d7_mp_gainloss)

        m1_mp_gainloss = dict_stats_1m_ago.get(set_code)
        m1_change_p = calculate_change(today_mp_gainloss, m1_mp_gainloss)
        
        get_first_gainloss_mp = list(SetSimulatedPriceStats.objects.filter(set=stat_today.set).values_list('booster_gainloss_mp', flat=True))
        get_first_gainloss_mp = [i for i in get_first_gainloss_mp if i != None][0]
        all_time_change_p = calculate_change(today_mp_gainloss, get_first_gainloss_mp)

        SetGainLossRanking.objects.update_or_create(
            set=stat_today.set,
            ranking_date=today,
            defaults={
                'mp_gl_ranking':ranking,
                'mp_gl_today': today_mp_gainloss,
                'mp_gl_week': d7_change_p,
                'mp_gl_month': m1_change_p,
                'mp_gl_all_time': all_time_change_p
            }
        )
        ranking += 1
        
def save_gainloss_rankings_ml():
    
    today = date.today()
    seven_days_ago = date.today() - timedelta(days=7)
    one_month_ago = date.today() - relativedelta.relativedelta(months=1)

    stats_today = SetSimulatedPriceStats.objects.filter(date_simulated=today).order_by('-booster_gainloss_ml')
    stats_7d_ago = SetSimulatedPriceStats.objects.filter(date_simulated=seven_days_ago)
    stats_1m_ago = SetSimulatedPriceStats.objects.filter(date_simulated=one_month_ago)

    dict_stats_today = {stat.set.code: stat.booster_gainloss_ml for stat in stats_today}
    dict_stats_7d_ago = {stat.set.code: stat.booster_gainloss_ml for stat in stats_7d_ago}
    dict_stats_1m_ago = {stat.set.code: stat.booster_gainloss_ml for stat in stats_1m_ago}
    ranking = 1
    for stat_today in stats_today:
        set_code = stat_today.set.code
        
        today_ml_gainloss = SetSimulatedPriceStats.objects.filter(set__code=set_code).filter(date_simulated=today).last().booster_gainloss_ml
        d7_ml_gainloss = dict_stats_7d_ago.get(set_code)
        d7_change_p = calculate_change(today_ml_gainloss, d7_ml_gainloss)

        m1_ml_gainloss = dict_stats_1m_ago.get(set_code)
        m1_change_p = calculate_change(today_ml_gainloss, m1_ml_gainloss)
        
        get_first_gainloss_ml = list(SetSimulatedPriceStats.objects.filter(set=stat_today.set).values_list('booster_gainloss_ml', flat=True))
        get_first_gainloss_ml = [i for i in get_first_gainloss_ml if i != None][0]
        all_time_change_p = calculate_change(today_ml_gainloss, get_first_gainloss_ml)

        SetGainLossRanking.objects.update_or_create(
            set=stat_today.set,
            ranking_date=today,
            defaults={
                'ml_gl_ranking':ranking,
                'ml_gl_today': today_ml_gainloss,
                'ml_gl_week': d7_change_p,
                'ml_gl_month': m1_change_p,
                'ml_gl_all_time': all_time_change_p
            }
        )
        ranking += 1

def update_ranking_change():
    today = date.today()
    yesterday = date.today() - timedelta(days=1)

    todayrankings = SetRankings.objects.filter(ranking_date=today)
    yesterday_rankings = SetRankings.objects.filter(ranking_date=yesterday)

    for ranking in todayrankings:
        mp_rank_today = ranking.mp_ranking
        mp_rank_yesterday = yesterday_rankings.get(set=ranking.set).mp_ranking
        mp_ranking_change = mp_rank_yesterday - mp_rank_today
        ranking.mp_ranking_change = mp_ranking_change

        ml_rank_today = ranking.ml_ranking
        ml_rank_yesterday = yesterday_rankings.get(set=ranking.set).ml_ranking
        ml_ranking_change = ml_rank_yesterday - ml_rank_today
        ranking.ml_ranking_change = ml_ranking_change
        ranking.save()
    print('updated ranking changes')

def update_ranking_change():
    today = date.today()
    yesterday = date.today() - timedelta(days=1)

    todayrankings = SetRankings.objects.filter(ranking_date=today)
    yesterday_rankings = SetRankings.objects.filter(ranking_date=yesterday)

    for ranking in todayrankings:
        mp_rank_today = ranking.mp_ranking
        mp_rank_yesterday = yesterday_rankings.get(set=ranking.set).mp_ranking
        mp_ranking_change = mp_rank_yesterday - mp_rank_today
        ranking.mp_ranking_change = mp_ranking_change

        ml_rank_today = ranking.ml_ranking
        ml_rank_yesterday = yesterday_rankings.get(set=ranking.set).ml_ranking
        ml_ranking_change = ml_rank_yesterday - ml_rank_today
        ranking.ml_ranking_change = ml_ranking_change
        ranking.save()
    print('updated ranking changes')


def update_gl_ranking_change():
    today = date.today()
    yesterday = date.today() - timedelta(days=1)

    todayrankings = SetGainLossRanking.objects.filter(ranking_date=today)
    yesterday_rankings = SetGainLossRanking.objects.filter(ranking_date=yesterday)

    for ranking in todayrankings:
        mp_rank_today = ranking.mp_gl_ranking
        mp_rank_yesterday = yesterday_rankings.get(set=ranking.set).mp_gl_ranking
        mp_ranking_change = mp_rank_yesterday - mp_rank_today
        ranking.mp_ranking_change = mp_ranking_change

        ml_rank_today = ranking.ml_gl_ranking
        ml_rank_yesterday = yesterday_rankings.get(set=ranking.set).ml_gl_ranking
        ml_ranking_change = ml_rank_yesterday - ml_rank_today
        ranking.ml_ranking_change = ml_ranking_change
        ranking.save()
    print('updated ranking changes')