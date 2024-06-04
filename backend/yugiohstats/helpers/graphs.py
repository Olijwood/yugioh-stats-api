from sets.models import Set, SetSimulatedPriceStats, SetGainLossRanking
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from .utils import get_set_data_directory
import math
from matplotlib.dates import DateFormatter
import numpy as np
import os
from datetime import timedelta, date

def round_up_to_nearest_x(number, x):
    return math.ceil(number / x) * x


def round_down_to_nearest_x(number, x):
    return math.floor(number / x) * x
    
def get_list_yticks(min_ml, max_mp):
    diff = max_mp - min_ml
    if diff >= 200:
        min_tick = round_down_to_nearest_x(min_ml, 20)
        max_tick = round_up_to_nearest_x(max_mp, 20)
        return [tick for tick in range(int(min_tick), int(max_tick) + 1, 20) if tick % 20 == 0]
    elif diff >= 100:
        min_tick = round_down_to_nearest_x(min_ml, 10)
        max_tick = round_up_to_nearest_x(max_mp, 10)
        return [tick for tick in range(int(min_tick), int(max_tick) + 1, 10) if tick % 10 == 0]
    elif diff >= 50:
        min_tick = round_down_to_nearest_x(min_ml, 5)
        max_tick = round_up_to_nearest_x(max_mp, 5)
        return [tick for tick in range(int(min_tick), int(max_tick) + 1, 5) if tick % 5 == 0]
    else:
        min_tick = round_down_to_nearest_x(min_ml, 2.5)
        max_tick = round_up_to_nearest_x(max_mp, 2.5)
        return [tick for tick in np.arange(min_tick, max_tick + 0.1, 2.5) if tick % 2.5 == 0]
    
def create_update_set_graphs(set_code):
    set_data_directory = get_set_data_directory(set_code)
    if set_data_directory is None:
        print('Set Code provided is not valid')
        return None

    data = []
    set_stats = SetSimulatedPriceStats.objects.filter(set__code=set_code)
    for stat in set_stats:
        data.append({
            'date_simulated': stat.date_simulated,
            'booster_mean_marketp': stat.booster_mean_marketp,
            'booster_median_marketp': stat.booster_median_marketp,
            'chance_greater_opened_value_marketp': stat.chance_greater_opened_value_marketp,
            'booster_mean_minlisting': stat.booster_mean_minlisting,
            'booster_median_minlisting': stat.booster_median_minlisting,
            'chance_greater_opened_value_minlisting': stat.chance_greater_opened_value_minlisting,
        })
    print(set_code)
    if data == []:
        print(f'No SetStats data for {set_code}')
        return None
    df = pd.DataFrame(data)
    df = df.groupby('date_simulated').mean().reset_index()
    df['date_simulated'] = pd.to_datetime(df['date_simulated'])
    df.set_index('date_simulated', inplace=True)

    # Get Min Max values for Y-Axis functions
    min_booster_mean_minlisting = df['booster_mean_minlisting'].min()
    min_booster_median_minlisting = df['booster_median_minlisting'].min()
    min_cgv_minlisting = df['chance_greater_opened_value_minlisting'].min()
    
    max_booster_mean_marketp = df['booster_mean_marketp'].max()
    max_booster_median_marketp = df['booster_median_marketp'].max()
    max_cgv_marketp = df['chance_greater_opened_value_marketp'].max()
    
    # Get Mean (Market Price vs Min Listing) Graph
    # Set the seaborn style
    sns.set_style("whitegrid")
    
    # Create a new figure with a specific size
    plt.figure(figsize=(12, 6))
    
    # Plot Mean Market Price as a line
    sns.lineplot(data=df['booster_mean_marketp'], color='blue', label='Mean Market Price', linestyle='-')
    
    # Plot dots for Mean Market Price
    sns.scatterplot(data=df['booster_mean_marketp'], color='blue', label='_nolegend_', marker='o')
    
    # Plot Mean Minimum Listing as a line
    sns.lineplot(data=df['booster_mean_minlisting'], color='green', label='Mean Minimum Listing', linestyle='-')
    
    # Plot dots for Mean Minimum Listing
    sns.scatterplot(data=df['booster_mean_minlisting'], color='green', label='_nolegend_', marker='o')
    
    # Set x-axis label
    plt.xlabel('Date Simulated', fontsize=12)
    
    # Set y-axis label
    plt.ylabel('Price ($)', fontsize=12)
    
    # Set plot title
    plt.title(f'{set_code} Simulated Mean Booster Price Over Time (MP/ML)', fontsize=14, weight='bold', y=1.025)
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=22.5)

    # Format x-axis date labels
    date_form = DateFormatter("%d/%m/%y")
    plt.gca().xaxis.set_major_formatter(date_form)
    
    # Set y-axis tick labels
    mean_list_yticks = get_list_yticks(min_ml=min_booster_mean_minlisting, max_mp=max_booster_mean_marketp)
    plt.yticks(mean_list_yticks)
    plt.gca().set_yticklabels(['%.2f' % ytick for ytick in mean_list_yticks])
    
    # Add legend
    plt.legend(fontsize=10)
    
    # Set x-axis limit
    plt.xlim(df.index[0], None)
    
    # Adjust layout to prevent overlapping labels
    plt.tight_layout()

    mean_filename = f'mean-graph{set_code}.jpg'
    mean_filepath = os.path.join(set_data_directory, mean_filename)
    plt.savefig(mean_filepath, format='jpg', dpi=72)
    plt.close()
    # Get Median (Market Price vs Min Listing) Graph

    df_filtered = df.dropna(subset=['booster_median_marketp', 'booster_median_minlisting'], how='all')
    unique_dates = df_filtered.index.drop_duplicates()
    # Set the seaborn style
    sns.set_style("whitegrid")
    
    # Create a new figure with a specific size
    plt.figure(figsize=(12, 6))
    
    # Plot Mean Market Price as a line
    sns.lineplot(data=df_filtered['booster_median_marketp'], color='blue', label='Median Market Price', linestyle='-')
    
    # Plot dots for Mean Market Price
    sns.scatterplot(data=df_filtered['booster_median_marketp'], color='blue', label='_nolegend_', marker='o')
    
    # Plot Mean Minimum Listing as a line
    sns.lineplot(data=df_filtered['booster_median_minlisting'], color='green', label='Median Minimum Listing', linestyle='-')

    # Plot dots for Mean Minimum Listing
    sns.scatterplot(data=df_filtered['booster_median_minlisting'], color='green', label='_nolegend_', marker='o')
    
    # Set x-axis label
    plt.xlabel('Date Simulated', fontsize=12)
    
    # Set y-axis label
    plt.ylabel('Price ($)', fontsize=12)
    
    # Set plot title
    plt.title(f'{set_code} Simulated Median Booster Price Over Time (MP/ML)', fontsize=14, weight='bold', y=1.025)
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=22.5)
    
    # Format x-axis date labels
    date_form = DateFormatter("%d/%m/%y")
    plt.gca().xaxis.set_major_formatter(date_form)
    
    # Set y-axis tick labels
    mean_list_yticks = get_list_yticks(min_ml=min_booster_median_minlisting, max_mp=max_booster_median_marketp)
    plt.yticks(mean_list_yticks)
    plt.gca().set_yticklabels(['%.2f' % ytick for ytick in mean_list_yticks])
    
    # Add legend
    plt.legend(fontsize=10)
    
    # Set x-axis limit
    plt.xlim(unique_dates[0], None)
    
    # Adjust layout to prevent overlapping labels
    plt.tight_layout()

    median_filename = f'median-graph{set_code}.jpg'
    median_filepath = os.path.join(set_data_directory, median_filename)
    plt.savefig(median_filepath, format='jpg', dpi=72)
    plt.close()
    
    # Get Chance Greater Value (CGV) over time (MP/ML)
    
    # Set the Seaborn style
    sns.set_style("whitegrid")
    
    # Create a new figure with a specific size
    plt.figure(figsize=(12, 6))
    
    # Plot Market Price Chance as a line
    sns.lineplot(x=df.index, y=df['chance_greater_opened_value_marketp'], color='blue', linewidth=2, label='Market Price Chance', linestyle='-')
    
    # Plot Minimum Listing Chance as a line
    sns.lineplot(x=df.index, y=df['chance_greater_opened_value_minlisting'], color='green', linewidth=2, label='Minimum Listing Chance', linestyle='-')
    
    # Plot dots for Market Price Chance
    sns.scatterplot(x=df.index, y=df['chance_greater_opened_value_marketp'], color='blue', edgecolor='white', zorder=2, s=50, marker='o')
    
    # Plot dots for Minimum Listing Chance
    sns.scatterplot(x=df.index, y=df['chance_greater_opened_value_minlisting'], color='green', edgecolor='white', zorder=2, s=50, marker='o')
    
    # Set x-axis label
    plt.xlabel('Date Simulated', fontsize=12)
    
    # Set y-axis label
    plt.ylabel('Chance (%)', fontsize=12)
    
    # Set plot title
    plt.title(f'{set_code} Comparison of Market Price Chance and Minimum Listing Chance Over Time', fontsize=14, weight='bold', y=1.025)
    
    # Customize legend
    plt.legend(fontsize=10)
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=22.5)
    
    # Format x-axis date labels
    date_form = DateFormatter("%d/%m/%y")
    plt.gca().xaxis.set_major_formatter(date_form)
    
    # Set y-axis tick labels
    yticks = get_list_yticks(min_cgv_minlisting, max_cgv_marketp)
    plt.yticks(yticks)
    # Adjust layout to prevent overlapping labels
    plt.tight_layout()

    cgv_filename = f'cgv-graph{set_code}.jpg'
    cgv_filepath = os.path.join(set_data_directory, cgv_filename)
    plt.savefig(cgv_filepath, format='jpg', dpi=72)
    plt.close()
    return 1

def create_update_sets_gl_graphs():
    set_codes = [set.code for set in Set.objects.all() if list(set.setgainlossranking_set.all()) != []]
    for set_code in set_codes:
        set_data_directory = get_set_data_directory(set_code)
        if set_data_directory is None:
            print('Set Code provided is not valid')
        data = []
        set_stats = SetGainLossRanking.objects.filter(set__code=set_code)
        for stat in set_stats:
            data.append({
                'ranking_date': stat.ranking_date,
                'mp_gl_today': stat.mp_gl_today,
                'ml_gl_today': stat.ml_gl_today,
            })
        df = pd.DataFrame(data)
        df = df.groupby('ranking_date').mean().reset_index()
        df['ranking_date'] = pd.to_datetime(df['ranking_date'])
        df.set_index('ranking_date', inplace=True)
        print(len(df))
        
        min_gl_ml = df['ml_gl_today'].min()
        min_gl_mp = df['mp_gl_today'].min()
        if min_gl_mp < min_gl_ml:
            min_gl_ml = min_gl_mp
        max_gl_mp = df['mp_gl_today'].max()

        sns.set_style("whitegrid")
    
        # Create a new figure with a specific size
        plt.figure(figsize=(12, 6))
        
        # Plot Mean Market Price as a line
        sns.lineplot(data=df['mp_gl_today'], color='blue', label='Gain/Loss Market Price', linestyle='-')

        # Plot dots for Mean Market Price
        sns.scatterplot(data=df['mp_gl_today'], color='blue', label='_nolegend_', marker='o')
        
        # Plot Mean Minimum Listing as a line
        sns.lineplot(data=df['ml_gl_today'], color='green', label='Gain/Loss Minimum Listing', linestyle='-')
        
        # Plot dots for Mean Minimum Listing
        sns.scatterplot(data=df['ml_gl_today'], color='green', label='_nolegend_', marker='o')

        # Set x-axis label
        plt.xlabel('Date Simulated', fontsize=12)
        
        # Set y-axis label
        plt.ylabel('Price ($)', fontsize=12)
        
        # Set plot title
        plt.title(f'{set_code} Simulated Gain/Loss($) Booster Price Over Time (MP/ML)', fontsize=14, weight='bold', y=1.025)
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=22.5)
    
        # Format x-axis date labels
        date_form = DateFormatter("%d/%m/%y")
        plt.gca().xaxis.set_major_formatter(date_form)

        # Set y-axis tick labels
        list_yticks = get_list_yticks(min_ml=min_gl_ml, max_mp=max_gl_mp)
        plt.yticks(list_yticks)
        plt.gca().set_yticklabels(['%.2f' % ytick for ytick in list_yticks])
        
        # Add legend
        plt.legend(fontsize=10)

        # Adjust layout to prevent overlapping labels
        plt.tight_layout()

        gl_filename = f'gl-graph{set_code}.jpg'
        gl_filepath = os.path.join(set_data_directory, gl_filename)
        plt.savefig(gl_filepath, format='jpg', dpi=72)
    print('Created/Updated all Gain/Loss graphs')