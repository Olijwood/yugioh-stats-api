from celery import shared_task
import requests
import time 

from ct_games.models import Game
from ct_cards.models import CardBlueprint
from helpers import get_auth_headers

from .models import Expansion
from .rankings import save_gl_rankings, save_cgv_rankings, update_ranking_change

from .simulators import (simulate_multiple_core_boxes, simulate_multiple_collector_without_qcr_boxes,
                         simulate_multiple_ra01_boxes, simulate_multiple_ra02_boxes,
                         simulate_multiple_collector_with_qcr_boxes, simulate_multiple_bol_with_qcr_boxes,
                         simulate_multiple_bol_with_starlight_boxes, simulate_multiple_core_with_starlight_boxes)
from .stats import (get_stats_for_simulated_set, exp_save_stats_to_model)
from .utils import (save_totals_to_csv)


@shared_task
def update_expansions():
    headers = get_auth_headers()
    endpoint = 'https://api.cardtrader.com/api/v2/expansions'
    yugioh_id = Game.objects.get(name='Yu-Gi-Oh!').id
    json = {'game_id': yugioh_id}
    get_response = requests.get(endpoint, json, headers=headers)
    expansions_status_code = get_response.status_code
    expansions_json = get_response.json()
    ygo_expansions_array = [expansion for expansion in expansions_json if expansion['game_id'] == yugioh_id]
    if expansions_status_code == 200:
        created_updated = False
        for ygo_expansion in ygo_expansions_array:
            expansion_obj, created = Expansion.objects.update_or_create(
                    id = ygo_expansion['id'],
                    game = Game.objects.get(id=yugioh_id),
                    name = ygo_expansion['name'],
                    defaults={
                        'code': ygo_expansion['code']
                    }
                )
            if created:
                print(f'Expansion: {expansion_obj.name} created')
                created_updated = True
            elif expansion_obj.code != ygo_expansion['code']:
                expansion_obj.code = ygo_expansion['code']
                expansion_obj.save()
                created_updated = True
                print(f'Expansion: {expansion_obj.name} updated')
        if created_updated:
            print('Expansions updated / created')
        else:
            print('Up to date! No Expansions created or updated')
    else:
        print('Get Expansions Request Failed')


def is_booster_box():
    headers = get_auth_headers()
    endpoint = 'https://api.cardtrader.com/api/v2/blueprints/export'
    exp_latest = list(Expansion.objects.filter(game__id=4).filter(is_booster_box=None))
    for exp in exp_latest:
        json = {'expansion_id': exp.id}
        get_response = requests.get(endpoint, json, headers=headers)
        blueprint_status_code = get_response.status_code
        if blueprint_status_code == 200:
            blueprint_json = get_response.json()
            if blueprint_json:
                bb_blueprints = [blueprint for blueprint in blueprint_json if (exp.name in blueprint['name'] and 'Booster Box' in blueprint['name'])]
                if bb_blueprints != []:
                    exp.is_booster_box = True
                    exp.save()
                    print(f'{exp.code}: is booster box')
                else:
                    exp.is_booster_box = False
                    exp.save()
                    print(f'{exp.code}: No Booster Box Blueprint')
            else:
                print(f'{exp.code} no json')
        else:
            print(f'{exp.code}: Error {blueprint_status_code}')

@shared_task
def get_latest_booster_prices():
    is_booster_box()
    headers = get_auth_headers()
    endpoint = 'https://api.cardtrader.com/api/v2/blueprints/export'
    exp_latest_boosters = list(Expansion.objects.filter(game__id=4).filter(is_booster_box=True))[-50:]
    for exp in exp_latest_boosters:
        time.sleep(0.5)
        json = {'expansion_id': exp.id}
        get_response = requests.get(endpoint, json, headers=headers)
        blueprint_status_code = get_response.status_code
        if blueprint_status_code == 200:
            blueprint_json = get_response.json()
            bb_blueprints = [blueprint for blueprint in blueprint_json if (exp.name in blueprint['name'] and 'Booster Box' in blueprint['name'])]
            if bb_blueprints != []:
                exp.is_booster_box = True
                exp.save()
                bb_blueprint = bb_blueprints[0]
                bb_endpoint = 'https://api.cardtrader.com/api/v2/marketplace/products'
                bb_id = bb_blueprint['id']
                bb_json = {'blueprint_id': bb_id,
                       'language': 'en'}
                bprint_get_response = requests.get(bb_endpoint, bb_json, headers=headers)
                print(exp.code, bprint_get_response.status_code)
                if bprint_get_response.status_code != 200:
                    print(f'{exp.code}: No listings for Booster Box')
                    continue
                bb_products_list = bprint_get_response.json()[str(bb_blueprint['id'])]
                if bb_products_list != []:
                    bb_price_dict = bb_products_list[0]['price']
                    print(bb_id)
                    exp.bb_blueprint_id = bb_id
                    price_to_float = bb_price_dict['cents']/100
                    exp.min_price_gbp = price_to_float
                    exp.min_price_gbp_formatted = bb_price_dict['formatted']
                    exp.save()
                    print(f'Updated Booster Price details for {exp.name}')
                else:
                    print(f'{exp.code}: No listings for Booster Box')
            else:
                exp.is_booster_box = False
                exp.save()
                print(f'{exp.code}: No Booster Box Blueprint')
        else:
            print(f'{exp.code}: Failed to get blueprints')
    return

@shared_task
def simulate_yugioh_core_qcr_stats():
    qcr_core_set_code_strings = ['phni', 'agov', 'dune', 'lede']
    num_iterations = 100000
    exp_stats_data = []
    for qcr_core_set_string in qcr_core_set_code_strings:
        qcr_core_set = Expansion.objects.get(code=qcr_core_set_string)
        cards_qcr_core_set = CardBlueprint.objects.filter(expansion=qcr_core_set)
        set_booster_price = qcr_core_set.min_price_gbp
        parsed_qcr_core_set = [[card.yugioh_rarity, card.get_price()] for card in cards_qcr_core_set if card.get_price() != None]
        
        simulated_totals = simulate_multiple_core_boxes(parsed_qcr_core_set, num_iterations)
        save_totals_to_csv(qcr_core_set_string, simulated_totals)
        set_booster_stats_data = get_stats_for_simulated_set(qcr_core_set_string, set_booster_price)
        exp_stats_data.append({
                'exp_id': qcr_core_set.id,
                'stats_data': set_booster_stats_data,
            })
        print(f'Successfully simulated {qcr_core_set_string} ')
    exp_save_stats_to_model(exp_stats_data)
    print('Saved qcr core expansion stats to model')
    return

@shared_task
def simulate_yugioh_rarity_ii_booster_stats():
    ra02 = Expansion.objects.get(code='ra02')
    ra02_cards = CardBlueprint.objects.filter(expansion=ra02)
    num_iterations = 100000
    exps_stats_data = []
    set_booster_price = ra02.min_price_gbp
    set_code = ra02.code

    parsed_ra02 = [[card.yugioh_rarity, card.get_price()] for card in ra02_cards if card.get_price() != None]

    simulated_totals = simulate_multiple_ra02_boxes(parsed_ra02, num_iterations)
    save_totals_to_csv(set_code, simulated_totals)
    exp_stats_data = get_stats_for_simulated_set(set_code, set_booster_price)

    exps_stats_data.append({
        'exp_id': ra02.id,
        'stats_data': exp_stats_data
    })
    exp_save_stats_to_model(exps_stats_data)
    print('Saved Simulated RA02 stats to model')
    return

@shared_task
def simulate_yugioh_rarity_i_booster_stats():
    ra01 = Expansion.objects.get(code='ra01')
    ra01_cards = CardBlueprint.objects.filter(expansion=ra01)
    num_iterations = 100000
    exps_stats_data = []
    set_booster_price = ra01.min_price_gbp
    set_code = ra01.code

    parsed_ra01 = [[card.yugioh_rarity, card.get_price()] for card in ra01_cards if card.get_price() != None]

    simulated_totals = simulate_multiple_ra01_boxes(parsed_ra01, num_iterations)
    save_totals_to_csv(set_code, simulated_totals)
    exp_stats_data = get_stats_for_simulated_set(set_code, set_booster_price)

    exps_stats_data.append({
        'exp_id': ra01.id,
        'stats_data': exp_stats_data
    })
    exp_save_stats_to_model(exps_stats_data)
    print('Saved Simulated RA01 stats to model')
    return

@shared_task
def simulate_yugioh_collector_without_qcr_booster_stats():
    codes_cllrctr_no_qcr = ['wisu', 'maze', 'amde', 'tama', 'grcr', 'angu', 'geim', 'toch']#no qcr
    exps_stats_data = []
    num_iterations = 100000

    for exp_code in codes_cllrctr_no_qcr:
        exp = Expansion.objects.get(code=exp_code)
        exp_cards = CardBlueprint.objects.filter(expansion=exp)
        booster_price = exp.min_price_gbp

        parsed_exp_cards = [[card.yugioh_rarity, card.get_price()] for card in exp_cards if card.get_price() != None]

        simulated_totals = simulate_multiple_collector_without_qcr_boxes(parsed_exp_cards, num_iterations)
        save_totals_to_csv(exp_code, simulated_totals)
        exp_stats_data = get_stats_for_simulated_set(exp_code, booster_price)
        exps_stats_data.append({
            'exp_id': exp.id,
            'stats_data': exp_stats_data
        })
        print(f'Successfully simulated {exp_code} ')
    exp_save_stats_to_model(exps_stats_data)
    print('Saved stats data for Yugioh Collector Sets without a QCR')
    return

@shared_task
def simulate_yugioh_collector_with_qcr_booster_stats():
    codes_cllrctr_qcr = ['vasm', 'mzmi']
    exps_stats_data = []
    num_iterations = 100000

    for exp_code in codes_cllrctr_qcr:
        exp = Expansion.objects.get(code=exp_code)
        exp_cards = CardBlueprint.objects.filter(expansion=exp)
        booster_price = exp.min_price_gbp

        parsed_exp_cards = [[card.yugioh_rarity, card.get_price()] for card in exp_cards if card.get_price() != None]

        simulated_totals = simulate_multiple_collector_with_qcr_boxes(parsed_exp_cards, num_iterations)
        save_totals_to_csv(exp_code, simulated_totals)
        exp_stats_data = get_stats_for_simulated_set(exp_code, booster_price)
        exps_stats_data.append({
            'exp_id': exp.id,
            'stats_data': exp_stats_data
        })
        print(f'Successfully simulated {exp_code} ')
    exp_save_stats_to_model(exps_stats_data)
    print('Saved stats data for Yugioh Collector Sets with a QCR')
    return

@shared_task
def simulate_yugioh_bol_with_qcr_booster_stats():
    codes_bol_qcr = ['blmr']
    exps_stats_data = []
    num_iterations = 100000

    for exp_code in codes_bol_qcr:
        exp = Expansion.objects.get(code=exp_code)
        exp_cards = CardBlueprint.objects.filter(expansion=exp)
        booster_price = exp.min_price_gbp

        parsed_exp_cards = [[card.yugioh_rarity, card.get_price()] for card in exp_cards if card.get_price() != None]

        simulated_totals = simulate_multiple_bol_with_qcr_boxes(parsed_exp_cards, num_iterations)
        save_totals_to_csv(exp_code, simulated_totals)
        exp_stats_data = get_stats_for_simulated_set(exp_code, booster_price)
        exps_stats_data.append({
            'exp_id': exp.id,
            'stats_data': exp_stats_data
        })
        print(f'Successfully simulated {exp_code} ')
    exp_save_stats_to_model(exps_stats_data)
    print('Saved stats data for Yugioh BOL Sets with QCR')
    return

@shared_task
def simulate_yugioh_bol_with_starlight_booster_stats():
    codes_bol_starlight = ['blcr', 'blar', 'brol']
    exps_stats_data = []
    num_iterations = 100000

    for exp_code in codes_bol_starlight:
        exp = Expansion.objects.get(code=exp_code)
        exp_cards = CardBlueprint.objects.filter(expansion=exp)
        booster_price = exp.min_price_gbp

        parsed_exp_cards = [[card.yugioh_rarity, card.get_price()] for card in exp_cards if card.get_price() != None]

        simulated_totals = simulate_multiple_bol_with_starlight_boxes(parsed_exp_cards, num_iterations)
        save_totals_to_csv(exp_code, simulated_totals)
        exp_stats_data = get_stats_for_simulated_set(exp_code, booster_price)
        exps_stats_data.append({
            'exp_id': exp.id,
            'stats_data': exp_stats_data
        })
        print(f'Successfully simulated {exp_code} ')
    exp_save_stats_to_model(exps_stats_data)
    print('Saved stats data for Yugioh BOL Sets with Starlight')
    return

@shared_task
def simulate_yugioh_core_with_starlight_booster_stats():
    codes_core_starlight = ['rotd', 'phra', 'blvo', 
                            'liov', 'dama', 'bode', 
                            'bach', 'difo', 'dabl', 
                            'phhy', 'pote', 'cyac']
    exps_stats_data = []
    num_iterations = 100000

    for exp_code in codes_core_starlight:
        exp = Expansion.objects.get(code=exp_code)
        exp_cards = CardBlueprint.objects.filter(expansion=exp)
        booster_price = exp.min_price_gbp

        parsed_exp_cards = [[card.yugioh_rarity, card.get_price()] for card in exp_cards if card.get_price() != None]

        simulated_totals = simulate_multiple_core_with_starlight_boxes(parsed_exp_cards, num_iterations)
        save_totals_to_csv(exp_code, simulated_totals)
        exp_stats_data = get_stats_for_simulated_set(exp_code, booster_price)
        exps_stats_data.append({
            'exp_id': exp.id,
            'stats_data': exp_stats_data
        })
        print(f'Successfully simulated {exp_code} ')
    exp_save_stats_to_model(exps_stats_data)
    print('Saved stats data for Yugioh Core Sets with Starlight')
    return

@shared_task
def update_rankings():
    save_gl_rankings()
    save_cgv_rankings()
    update_ranking_change()
    print('updated rankings')
    return
