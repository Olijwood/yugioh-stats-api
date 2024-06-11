import csv
from datetime import date, timedelta
import os
import pandas as pd
from pathlib import Path

from .models import Expansion, ExpSimulatedPriceStats

BASE_DIR =  Path(__file__).resolve().parent.parent


def save_totals_to_csv(set_code, results):
    set_code = str(set_code).upper()
    directory = os.path.join(BASE_DIR, 'staticfiles-cdn', 'sets-data', set_code, 'data')
    os.makedirs(directory, exist_ok=True)

   
    filename = set_code + '.csv'
    filepath = os.path.join(directory, filename)

    with open(filepath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Total'])  # Write the header
        for result in results:
            writer.writerow([result])
        
def get_valid_set_codes():
    set_codes_raw = Expansion.objects.values_list('code', flat=True)
    set_codes = [set_code for set_code in set_codes_raw if set_code != None]
    return set_codes

def get_set_data_directory(set_code):
    valid_set_codes = get_valid_set_codes()
    if set_code not in valid_set_codes:
        print('Invalid Set Code')
        return None
    set_code = str(set_code).upper()
    directory = os.path.join(BASE_DIR, 'staticfiles-cdn', 'sets-data', set_code, 'data')
    os.makedirs(directory, exist_ok=True)
    return directory