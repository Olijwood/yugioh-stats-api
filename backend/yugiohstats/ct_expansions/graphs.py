import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import math
from matplotlib.dates import DateFormatter
import numpy as np
import os
from datetime import timedelta, date

from .models import ExpSimulatedPriceStats
from .utils import get_set_data_directory

def round_up_to_nearest_x(number, x):
    return math.ceil(number / x) * x


def round_down_to_nearest_x(number, x):
    return math.floor(number / x) * x
    
def get_list_yticks(min, max):
    diff = max - min
    if diff >= 200:
        min_tick = round_down_to_nearest_x(min, 20)
        max_tick = round_up_to_nearest_x(max, 20)
        return [tick for tick in range(int(min_tick), int(max_tick) + 1, 20) if tick % 20 == 0]
    elif diff >= 100:
        min_tick = round_down_to_nearest_x(min, 10)
        max_tick = round_up_to_nearest_x(max, 10)
        return [tick for tick in range(int(min_tick), int(max_tick) + 1, 10) if tick % 10 == 0]
    elif diff >= 50:
        min_tick = round_down_to_nearest_x(min, 5)
        max_tick = round_up_to_nearest_x(max, 5)
        return [tick for tick in range(int(min_tick), int(max_tick) + 1, 5) if tick % 5 == 0]
    elif diff >= 5:
        min_tick = round_down_to_nearest_x(min, 2.5)
        max_tick = round_up_to_nearest_x(max, 2.5)
        return [tick for tick in np.arange(min_tick, max_tick + 0.1, 2.5) if tick % 2.5 == 0]
    else:
        min_tick = round_down_to_nearest_x(min, 1)
        max_tick = round_up_to_nearest_x(max, 1)
        return [tick for tick in range(int(min_tick), int(max_tick) + 1, 1) if tick % 1 == 0]
   
    
def create_update_set_mean_median_graph(set_code):
    set_data_directory = get_set_data_directory(set_code)
    if set_data_directory is None:
        print('Set Code provided is not valid')
        return 0

    data = []
    exp_stats = ExpSimulatedPriceStats.objects.filter(expansion__code=set_code)
    for stat in exp_stats:
        data.append({
            'date_simulated': stat.date_simulated,
            'mean': stat.mean,
            'median': stat.median
        })
    if data == []:
        print(f'No SetStats data for {set_code}')
        return None
    df = pd.DataFrame(data)
    df = df.groupby('date_simulated').mean().reset_index()
    df['date_simulated'] = pd.to_datetime(df['date_simulated'])
    df.set_index('date_simulated', inplace=True)

    min = df['mean'].min()
    max = df['mean'].max()
    min_med = df['median'].min()
    max_med = df['median'].max()
    if min_med < min:
        min = min_med
    if max_med > max:
        max = max_med

    # Get Mean Graph
    # Set the seaborn style
    sns.set_style("whitegrid")

    # Create a new figure with a specific size
    plt.figure(figsize=(12, 6))
    
    # Plot Mean Market Price as a line
    sns.lineplot(data=df['mean'], color='blue', label='Mean Price (£)', linestyle='-', linewidth=2, )
    
    # Plot Mean Market Price as a line
    sns.lineplot(data=df['median'], color='green', label='Median Price (£)', linestyle='-', linewidth=2, )

    # Plot dots for Mean Market Price
    sns.scatterplot(data=df['mean'], color='blue', label='_nolegend_', marker='o', edgecolor='white', zorder=2, s=50,)
    
    # Plot dots for Mean Market Price
    sns.scatterplot(data=df['median'], color='green', label='_nolegend_', marker='o', edgecolor='white', zorder=2, s=50,)

    # Set x-axis label
    plt.xlabel('Date Simulated', fontsize=12)
    
    # Set y-axis label
    plt.ylabel('Price (£)', fontsize=12)
    
    # Set plot title
    plt.title(f'{set_code}: Mean vs Median Simulated Value Over Time (£)', fontsize=14, weight='bold', y=1.025)
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=22.5)

    # Format x-axis date labels
    date_form = DateFormatter("%d/%m/%y")
    plt.gca().xaxis.set_major_formatter(date_form)
    
    # Set y-axis tick labels
    mean_list_yticks = get_list_yticks(min, max)
    plt.yticks(mean_list_yticks)
    plt.gca().set_yticklabels(['%.2f' % ytick for ytick in mean_list_yticks])
    
    # Add legend
    plt.legend(fontsize=10)
    
    # Set x-axis limit
    plt.xlim(df.index[0], None)
    
    # Adjust layout to prevent overlapping labels
    plt.tight_layout()

    mean_filename = f'ct-mean-graph{set_code}.jpg'
    mean_filepath = os.path.join(set_data_directory, mean_filename)
    plt.savefig(mean_filepath, format='jpg', dpi=72)
    plt.close()

    return 1

def create_update_set_cgv_graph(set_code):
    set_data_directory = get_set_data_directory(set_code)
    if set_data_directory is None:
        print('Set Code provided is not valid')
        return 0

    data = []
    exp_stats = ExpSimulatedPriceStats.objects.filter(expansion__code=set_code)
    has_cgv = False
    for stat in exp_stats:
        data.append({
            'date_simulated': stat.date_simulated,
            'cgv': stat.cgv,
        })
        if stat.cgv != None:
            has_cgv = True
    if data == []:
        print(f'No SetStats data for {set_code}')
        return 0
    if has_cgv == False:
        print(f'No CGV data for {set_code}')
        return 0
    df = pd.DataFrame(data)
    df = df.groupby('date_simulated').mean().reset_index()
    df['date_simulated'] = pd.to_datetime(df['date_simulated'])
    df.set_index('date_simulated', inplace=True)

    min = df['cgv'].min()
    max = df['cgv'].max()
    # Get Chance Greater Value (CGV) over time 
    
    # Set the Seaborn style
    sns.set_style("whitegrid")
    
    # Create a new figure with a specific size
    plt.figure(figsize=(12, 6))
    
    # Plot Market Price Chance as a line
    sns.lineplot(x=df.index, y=df['cgv'], color='blue', linewidth=2, label='Chance', linestyle='-')
    
    # Plot dots for Market Price Chance
    sns.scatterplot(x=df.index, y=df['cgv'], color='blue', edgecolor='white', zorder=2, s=50, marker='o')
    
    # Set x-axis label
    plt.xlabel('Date', fontsize=12)
    
    # Set y-axis label
    plt.ylabel('Chance (%)', fontsize=12)
    
    # Set plot title
    plt.title(f'{set_code} Chance Greater Opened Value over time', fontsize=14, weight='bold', y=1.025)
    
    # Customize legend
    plt.legend(fontsize=10)
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=22.5)
    
    # Format x-axis date labels
    date_form = DateFormatter("%d/%m/%y")
    plt.gca().xaxis.set_major_formatter(date_form)
    
    # Set y-axis tick labels
    yticks = get_list_yticks(min, max)
    plt.yticks(yticks)
    # Adjust layout to prevent overlapping labels
    plt.tight_layout()

    cgv_filename = f'ct-cgv-graph{set_code}.jpg'
    cgv_filepath = os.path.join(set_data_directory, cgv_filename)
    plt.savefig(cgv_filepath, format='jpg', dpi=72)
    plt.close()
    return 1

def create_update_set_gainloss_graph(set_code):
    set_data_directory = get_set_data_directory(set_code)
    if set_data_directory is None:
        print('Set Code provided is not valid')
        return 0

    data = []
    exp_stats = ExpSimulatedPriceStats.objects.filter(expansion__code=set_code)
    has_gainloss = False
    for stat in exp_stats:
        data.append({
            'date_simulated': stat.date_simulated,
            'gainloss': stat.gainloss,
        })
        if stat.gainloss != None:
            has_gainloss = True
    if data == []:
        print(f'No SetStats data for {set_code}')
        return 0
    if has_gainloss == False:
        print(f'No gainloss data for {set_code}')
        return 0
    df = pd.DataFrame(data)
    df = df.groupby('date_simulated').mean().reset_index()
    df['date_simulated'] = pd.to_datetime(df['date_simulated'])
    df.set_index('date_simulated', inplace=True)

    min = df['gainloss'].min()
    max = df['gainloss'].max()
    # Get Gainloss (£) over time 
    
    # Set the Seaborn style
    sns.set_style("whitegrid")
    
    # Create a new figure with a specific size
    plt.figure(figsize=(12, 6))
    
    # Plot Market Price Chance as a line
    sns.lineplot(x=df.index, y=df['gainloss'], color='blue', linewidth=2, label='Gain / Loss', linestyle='-')
    
    # Plot dots for Market Price Chance
    sns.scatterplot(x=df.index, y=df['gainloss'], color='blue', edgecolor='white', zorder=2, s=50, marker='o')
    
    # Set x-axis label
    plt.xlabel('Date', fontsize=12)
    
    # Set y-axis label
    plt.ylabel('Gain / Loss (£)', fontsize=12)
    
    # Set plot title
    plt.title(f'{set_code} Opened Gain/Loss (£) over time', fontsize=14, weight='bold', y=1.025)
    
    # Customize legend
    plt.legend(fontsize=10)
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=22.5)
    
    # Format x-axis date labels
    date_form = DateFormatter("%d/%m/%y")
    plt.gca().xaxis.set_major_formatter(date_form)
    
    # Set y-axis tick labels
    yticks = get_list_yticks(min, max)
    plt.yticks(yticks)
    # Adjust layout to prevent overlapping labels
    plt.tight_layout()

    gainloss_filename = f'ct-gainloss-graph{set_code}.jpg'
    gainloss_filepath = os.path.join(set_data_directory, gainloss_filename)
    plt.savefig(gainloss_filepath, format='jpg', dpi=72)
    plt.close()
    return 1
