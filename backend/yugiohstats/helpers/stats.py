from datetime import date
import os
from pathlib import Path
import pandas as pd
from .utils import get_set_data_directory

BASE_DIR =  Path(__file__).resolve().parent.parent

def stats_for_simulated_set(simulated_values, set_booster_price):
    num_values = len(simulated_values)

    mean_value = round((sum(simulated_values) / len(simulated_values)),2)
    
    sorted_values = sorted(simulated_values)
    if num_values % 2 == 0:
        median_value = (sorted_values[num_values // 2 - 1] + sorted_values[num_values // 2]) / 2
    else:
        median_value = sorted_values[num_values // 2]


    higher_values = sum(value > set_booster_price for value in simulated_values)
    chance_higher_value = round((higher_values / num_values) * 100, 2)

    date_updated = date.today()

    set_data = {
        'mean_value': mean_value,
        'median_value': median_value,
        'chance_higher_value': chance_higher_value,
        'date_updated': date_updated
    }
    return set_data

def get_stats_for_simulated_set(set_code, MPorML, set_booster_price): 
    if (str(MPorML).lower() == 'mp' or 
        str(MPorML).lower() == 'ml'):
        MPorML = str(MPorML).lower()
        filepath = os.path.join(BASE_DIR, 'staticfiles-cdn', 
                                'sets-data', set_code, 
                                'data', f'{MPorML}{set_code}.csv')
        df = pd.read_csv(filepath)
        
        mean = round(df['Total'].mean(), 2)
        median = round(df['Total'].median(), 2)
        std_dev = df['Total'].std()
        num_values = len(df['Total'])

        higher_values = sum(value > set_booster_price for value in df['Total'])
        chance_higher_value = round((higher_values / num_values) * 100, 2)

        date_updated = date.today()

        set_data = {
        'mean_value': mean,
        'median_value': median,
        'chance_higher_value': chance_higher_value,
        'date_updated': date_updated
        }
        return set_data


    else:
        print('''Please use: \nMP for Market Price or \nML for mininum listing Price''')

def get_user_cgv_gainloss(set_code, user_booster_price):
    set_data_directory = get_set_data_directory(set_code)

    ml_filepath = os.path.join(set_data_directory, f'ml{set_code}.csv')
    mp_filepath = os.path.join(set_data_directory, f'mp{set_code}.csv')

    ml_df = pd.read_csv(ml_filepath)
    mp_df = pd.read_csv(mp_filepath)

    ml_len = len(ml_df['Total'])
    mp_len = len(mp_df['Total'])

    mp_difference = sum(mp_df['Total']) - (user_booster_price*mp_len)
    mp_gainloss = round((mp_difference/mp_len), 2)
    ml_difference = sum(ml_df['Total']) - (user_booster_price*ml_len)
    ml_gainloss = round((ml_difference/ml_len), 2)

    ml_sum_hv = sum(value > user_booster_price for value in ml_df['Total'])
    mp_sum_hv = sum(value > user_booster_price for value in mp_df['Total'])

    ml_chv = round((ml_sum_hv / ml_len) * 100, 2)
    mp_chv = round((mp_sum_hv / mp_len) * 100, 2)

    user_cgv_gainloss_data = [
    {'mp-cgv': mp_chv,
    'mp-gainloss': mp_gainloss},
    {'ml-cgv': ml_chv,
    'ml-gainloss': ml_gainloss}
    ]          
    return user_cgv_gainloss_data


