from datetime import date, timedelta
import os
import pandas as pd
from pathlib import Path

from .models import Expansion, ExpSimulatedPriceStats

BASE_DIR =  Path(__file__).resolve().parent.parent

def get_stats_for_simulated_set(set_code, set_booster_price): 
    set_code = str(set_code).upper()
    filepath = os.path.join(BASE_DIR, 'staticfiles-cdn', 
                            'sets-data', set_code, 
                            'data', f'{set_code}.csv')
    df = pd.read_csv(filepath)
    
    mean = round(df['Total'].mean(), 2)
    median = round(df['Total'].median(), 2)
    std_dev = df['Total'].std()
    num_values = len(df['Total'])
    total = sum(df['Total'])

    if set_booster_price is not None:
        higher_values = sum(value > set_booster_price for value in df['Total'])
        chance_higher_value = round((higher_values / num_values) * 100, 2)

        difference = total - (set_booster_price*num_values)
        gainloss = round((difference/num_values), 2)
    else:
        chance_higher_value = 'None'
        gainloss = 'None'

    date_updated = date.today()

    set_data = {
    'mean': mean,
    'median': median,
    'cgv': chance_higher_value,
    'date_simulated': date_updated,
    'gainloss': gainloss
    }
    return set_data

def exp_save_stats_to_model(exp_stats_data):
    for exp_stats in exp_stats_data:
        try:
            stats = exp_stats['stats_data']
            exp_obj = Expansion.objects.get(id=exp_stats['exp_id'])
            
            mean = stats['mean']
            median = stats['median']
            gainloss = stats['gainloss']
            cgv = stats['cgv']
            date =  stats['date_simulated']


            if (gainloss == 'None' or cgv == 'None'):
                gainloss = None
                cgv = None
            
            try:
                stats_obj = ExpSimulatedPriceStats.objects.filter(date_simulated=date).get(expansion=exp_obj)
                stats_obj.mean = round(((stats_obj.mean + mean) / 2), 2)
                stats_obj.median = round(((stats_obj.median + median) / 2), 2)

                if (cgv is None or 
                    gainloss is None):
                    stats_obj.save()

                elif (stats_obj.cgv is None or 
                    stats_obj.gainloss is None):
                    stats_obj.cgv = cgv
                    stats_obj.gainloss = gainloss
                    stats_obj.save()
                else:
                    stats_obj.gainloss = round(((stats_obj.gainloss + gainloss)/2), 2)
                    stats_obj.cgv = round(((stats_obj.cgv + cgv)/2), 2)
                    stats_obj.save()
                print(f'{exp_obj.code}: updated todays price stats')

            except ExpSimulatedPriceStats.DoesNotExist:
                

                ExpSimulatedPriceStats.objects.create(
                    expansion = exp_obj,
                    mean = mean,
                    median = median,
                    cgv = cgv,
                    gainloss = gainloss,
                    date_simulated = date,
                )
                print(f'Created simulated price stats for {exp_obj.name}')

        except Expansion.DoesNotExist:
            print('Expansion does not exist')
            continue