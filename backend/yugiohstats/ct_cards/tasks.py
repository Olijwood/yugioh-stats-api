from celery import shared_task
from ct_expansions.models import Expansion
from datetime import date
from helpers import get_auth_headers
import requests

from .models import CardBlueprint, CardPriceHistory
from .utils import parse_yugioh_rarity

@shared_task
def yugioh_exp_get_card_blueprints():
    sets = list(Expansion.objects.filter(game__id=4).filter(is_booster_box=True))[-45:]
    sets = [set for set in sets if 'OCG' not in set.name]
    headers = get_auth_headers()
    bprint_endpoint = 'https://api.cardtrader.com/api/v2/blueprints/export'
    
    for set in sets:
        print(set.name)
        bprint_json = {'expansion_id': set.id}
        
        bprint_response = requests.get(bprint_endpoint, json=bprint_json, headers=headers)
        print(bprint_response.status_code)
        
        if (bprint_response.status_code) == 200:
            set_bprints = bprint_response.json()
            set_bprints = [prod for prod in set_bprints if (
                set.name not in prod['name'] and 
                'collector_number' in prod['fixed_properties'])
            ]
            created_updated = False
            for prod in set_bprints:

                rarity = prod['version'] if prod['version'] != None else prod['fixed_properties']['yugioh_rarity']
                rarity = parse_yugioh_rarity(rarity=rarity, set_code=set.code)
                
                if prod['image'] != None:
                    img_url = prod['image']['url']
                else: 
                    img_url = 'https://cardtrader.com/fallbacks/card_uploader/preview.png'
                prod_obj, created = CardBlueprint.objects.update_or_create(
                    id = prod['id'],
                    expansion = set,
                    name =  prod['name'],
                    defaults = {
                        'yugioh_rarity': rarity,
                        'collector_number': prod['fixed_properties']['collector_number'],
                        'img_download_link': img_url,
                        
                    }
                )
                if created:
                        print(f'Product: {prod_obj.name} created')
                        created_updated = True
                elif (prod_obj.collector_number != prod['fixed_properties']['collector_number'] or
                      prod_obj.yugioh_rarity != rarity or
                      prod_obj.img_download_link != img_url
                     ):
                    prod_obj.collector_number = prod['fixed_properties']['collector_number']
                    prod_obj.yugioh_rarity= rarity
                    prod_obj.img_download_link = img_url
                    prod_obj.save()
                    created_updated = True
                    print(f'Product: {prod_obj.name} updated')
            if created_updated:
                print(f'{set.name}: Products updated / created')
            else:
                print(f'Up to date! No {set.name} Products: created or updated')
        else:
            print(f'Error - Status Code: {bprint_response.status_code}')
    return

@shared_task
def update_expansion_cards_prices():
    i=0
    headers = get_auth_headers()
    exp_ids = CardBlueprint.objects.values_list('expansion', flat=True).distinct()
    for exp_id in exp_ids:
        exp = Expansion.objects.get(id=exp_id)
        if 'jp' in exp.code:
            continue
        expmp_endpoint = 'https://api.cardtrader.com/api/v2/marketplace/products'
        expmp_json = {'language': 'en',
                      'expansion_id': exp_id}
        
        expmp_response = requests.get(expmp_endpoint, json=expmp_json, headers=headers)
        if expmp_response.status_code == 200:
            mp_json = expmp_response.json()

            bp_ids = list(exp.cardblueprint_set.values_list('id', flat=True))
            today = date.today()
            print(exp.name)
            for bp_id in bp_ids:
                card = CardBlueprint.objects.get(id=bp_id)
                cardprice_obj, created = CardPriceHistory.objects.update_or_create(
                    card=card,
                    defaults={
                        'date': today,
                    }
                )
                if str(bp_id) not in mp_json:
                    continue
                prod_list = mp_json[str(bp_id)]
            
                #first ed
                for prod in prod_list:
                    if ('yugioh_language' in prod['properties_hash'] and
                        'condition' in prod['properties_hash']):
                        if (prod['properties_hash']['yugioh_language'] == 'en' and
                            ('Near Mint' in prod['properties_hash']['condition'] or 
                             'Slightly Played' in prod['properties_hash']['condition'])):
                            first_ed = prod['properties_hash']['first_edition']
                            if first_ed == True:
                                
                                price = prod['price']
                                min_price_gbp = price['cents']/100
                                min_price_gbp_formatted = '£%.2f' %(min_price_gbp)
                                
                                cardprice_obj.min_price_gbp = min_price_gbp
                                cardprice_obj.min_price_gbp_formatted = min_price_gbp_formatted
                                cardprice_obj.save()
            
                                break
                #unlimited
                for prod in prod_list:
                    if ('yugioh_language' in prod['properties_hash'] and
                        'condition' in prod['properties_hash']):
                        if (prod['properties_hash']['yugioh_language'] == 'en' and
                            ('Near Mint' in prod['properties_hash']['condition'] or 
                             'Slightly Played' in prod['properties_hash']['condition'])):
                            first_ed = prod['properties_hash']['first_edition']
                            if first_ed == False:
                            
                                price = prod['price']
                                min_price_gbp = price['cents']/100
                                min_price_gbp_formatted = '£%.2f' %(min_price_gbp)
                                
                                cardprice_obj.unlim_min_price_gbp = min_price_gbp
                                cardprice_obj.unlim_min_price_gbp_formatted = min_price_gbp_formatted
                                cardprice_obj.save()
            
                                break
        else:
            print(f'{exp.name} error status code: {expmp_response.status_code}')
        i += 1
    print('FINISHED updating expansion card prices')
    print(i)
    return