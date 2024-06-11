from celery import shared_task
from .models import Game
import requests
from helpers import get_auth_headers

@shared_task
def update_games():
    endpoint = 'https://api.cardtrader.com/api/v2'
    headers = get_auth_headers()
    test_endpoint = endpoint + '/info'
    test_get_response = requests.get(test_endpoint, headers=headers)
    test_status_code = test_get_response.status_code
    if test_status_code == 200:
        print('Successfully tested CT-API authorization, updating CT games')
        endpoint = 'https://api.cardtrader.com/api/v2/games'
        get_response = requests.get(endpoint, headers=headers)
        games_status_code = get_response.status_code
        games_array = get_response.json()['array']
        print(games_status_code)
        print(games_array)
        if games_status_code == 200:
            created_updated = False
            for ct_game in games_array:
                game_obj, created = Game.objects.update_or_create(
                    id = ct_game['id'],
                    name = ct_game['name'],
                    defaults={
                        'display_name': ct_game['display_name']
                    }
                )
                if created:
                    print(f'Game: {game_obj.name} created')
                    created_updated = True
                elif game_obj.display_name != ct_game['display_name']:
                    game_obj.display_name = ct_game['display_name']
                    game_obj.save()
                    created_updated = True
                    print(f'Game: {game_obj.name} updated')
            if created_updated:
                print('Games updated / created')
            else:
                print('Up to date! No games created or updated')
        else:
            print('Get Games Request Failed')
    else:
        print('CT-API Authorization Failed')