import os
import csv
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from .validators import get_valid_set_codes


BASE_DIR =  Path(__file__).resolve().parent.parent



def get_set_data_directory(set_code):
    set_code = str(set_code).upper()
    valid_set_codes = get_valid_set_codes()
    if set_code not in valid_set_codes:
        print('Invalid Set Code')
        return None
    directory = os.path.join(BASE_DIR, 'staticfiles-cdn', 'sets-data', set_code, 'data')
    os.makedirs(directory, exist_ok=True)
    return directory
    
    
def last_word(string):
    # taking empty string
    newstring = ""
    
    # calculating length of string
    length = len(string)
    
    # traversing from last
    for i in range(length-1, -1, -1):  # Modify the range to include the first character
      
        # if space is occurred then return
        if(string[i] == " "):
            # if newstring is empty, it means there was no whitespace, return the entire string
            if not newstring:
                return string
            # return newstring
            return newstring
        else:
            newstring = string[i] + newstring  # append characters in reverse order

    # if the loop completes without finding whitespace, return the entire string
    return string

def save_results_to_csv(set_code, results, MPorML):
    directory = os.path.join(BASE_DIR, 'staticfiles-cdn', 'sets-data', set_code, 'data')
    os.makedirs(directory, exist_ok=True)

    if (str(MPorML).lower() == 'mp' or 
        str(MPorML).lower() == 'ml'):
        MPorML = str(MPorML).lower()
        filename = MPorML + set_code + '.csv'
        filepath = os.path.join(directory, filename)

        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Total'])  # Write the header
            for result in results:
                writer.writerow([result])
    else:
        print('''Please use: \nMP for Market Price or \nML for mininum listing Price''')

def read_results(set_code, MPorML):
    
    if (str(MPorML).lower() == 'mp' or 
        str(MPorML).lower() == 'ml'):
        MPorML = str(MPorML).lower()
        filepath = os.path.join(BASE_DIR, 'staticfiles-cdn', 
                                'sets-data', set_code, 
                                'data', f'{MPorML}{set_code}.csv')
        df = pd.read_csv(filepath)
        return df
    else:
        print('''Please use: \nMP for Market Price or \nML for mininum listing Price''')


def analyze_results(df):
    mean = df['Total'].mean()
    median = df['Total'].median()
    std_dev = df['Total'].std()
    percentiles = df['Total'].quantile([0.1, 0.25, 0.5, 0.75, 0.9]).to_list()

     # Display statistics
    print(f"Mean: ${mean:.2f}")
    print(f"Median: ${median:.2f}")
    print(f"Standard Deviation: {std_dev:.2f}")
    print(f"Percentiles (10%, 25%, 50%, 75%, 90%): {percentiles}")

    # Plot histogram
    plt.figure(figsize=(10, 6))
    plt.hist(df['Total'], bins='auto', alpha=0.7, color='blue')
    plt.title('Distribution of Booster Box Totals')
    plt.xlabel('Total Value ($)')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

results = []
for i in range(1, 51):
    results.append(i)

save_results_to_csv('RA02', results, 'MP')

def pct_str(pct):
    pct = '%.2f' %(float(pct))
    return pct + '%'

