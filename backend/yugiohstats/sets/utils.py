import os
from pathlib import Path

BASE_DIR =  Path(__file__).resolve().parent.parent

def get_set_data_directory(set_code):
    print(BASE_DIR)
    set_code = str(set_code).upper()
    directory = os.path.join(BASE_DIR, 'staticfiles-cdn', 'sets-data', set_code, 'data')
    os.makedirs(directory, exist_ok=True)
    return directory