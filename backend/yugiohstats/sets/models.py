from django.conf import settings
from django.db import models
from django.urls import reverse

import os

from .utils import get_set_data_directory

USER = settings.AUTH_USER_MODEL

LINKS_FOR_SETS_WITH_STATS = ['https://www.tcgplayer.com/search/yugioh/25th-anniversary-rarity-collection-ii',
 'https://www.tcgplayer.com/search/yugioh/legacy-of-destruction',
 'https://www.tcgplayer.com/search/yugioh/phantom-nightmare',
 'https://www.tcgplayer.com/search/yugioh/maze-of-millennia',
 'https://www.tcgplayer.com/search/yugioh/valiant-smashers',
 'https://www.tcgplayer.com/search/yugioh/25th-anniversary-rarity-collection',
 'https://www.tcgplayer.com/search/yugioh/age-of-overlord',
 'https://www.tcgplayer.com/search/yugioh/duelist-nexus',
 'https://www.tcgplayer.com/search/yugioh/battles-of-legend-monstrous-revenge',
 'https://www.tcgplayer.com/search/yugioh/wild-survivors',
 'https://www.tcgplayer.com/search/yugioh/cyberstorm-access',
 'https://www.tcgplayer.com/search/yugioh/maze-of-memories',
 'https://www.tcgplayer.com/search/yugioh/amazing-defenders',
 'https://www.tcgplayer.com/search/yugioh/tactical-masters',
 'https://www.tcgplayer.com/search/yugioh/the-grand-creators?',
 'https://www.tcgplayer.com/search/yugioh/kings-court?productLineName=yugioh&setName=kings-court',
 'https://www.tcgplayer.com/search/yugioh/ancient-guardians?productLineName=yugioh&page=1&setName=ancient-guardians',
 'https://www.tcgplayer.com/search/yugioh/genesis-impact?productLineName=yugioh&setName=genesis-impact',
 'https://www.tcgplayer.com/search/yugioh/toon-chaos']

class Set(models.Model):
    title = models.CharField(max_length=100, blank=True, 
                             null=True)
    link = models.URLField(blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, 
                            null=True)
    code = models.CharField(max_length=12, blank=True, 
                            null=True)
    average_price = models.DecimalField(max_digits=10, 
                            decimal_places=2, 
                            null=True, blank=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.link
    
    # def get_absolute_url(self):
    #     return reverse("set-detail", kwargs={"id": self.id})

    @property
    def average_price_in_sterling(self):
        if self.average_price is not None:
            return '£%.2f' %(float(self.average_price)/1.27)
        else:
            return None
    
    @property
    def price_with_dollar_sign(self):
        if self.average_price is not None:
            return '$%.2f' %(float(self.average_price))
        else:
            return None
    
    def get_latest_simulated_stats(self):
        if self.link in LINKS_FOR_SETS_WITH_STATS:
            latest_simulation = self.setsimulatedpricestats_set.order_by('-date_simulated').first()
            if latest_simulation:
                latest_stats = {
                    'set_name': str(latest_simulation.set.title),
                    'booster-mean': '$%.2f' %(float(latest_simulation.booster_mean)),
                    'booster-median': '$%.2f' %(float(latest_simulation.booster_median)),
                    'chance-higher-value': f'{float(latest_simulation.chance_greater_opened_value)}%',
                    'date-simulated': latest_simulation.date_simulated
                }
                return latest_stats
        else:
            return None
    
    def get_simulated_mean_latest(self):
        if self.link in LINKS_FOR_SETS_WITH_STATS:
            latest_simulation = self.setsimulatedpricestats_set.order_by('-date_simulated').first()
            if latest_simulation:
                return latest_simulation.booster_mean
        else:
            return None
        
    def get_simulated_median_latest(self):
        if self.link in LINKS_FOR_SETS_WITH_STATS:
            latest_simulation = self.setsimulatedpricestats_set.order_by('-date_simulated').first()
            if latest_simulation:
                return latest_simulation.booster_median
        else:
            return None
        
    def get_simulated_chance_higher_value_latest_mp(self):
        if self.link in LINKS_FOR_SETS_WITH_STATS:
            latest_simulation = self.setsimulatedpricestats_set.order_by('-date_simulated').first()
            if latest_simulation:
                return latest_simulation.chance_greater_opened_value_market_p
        else:
            return None
        
    def get_simulated_chance_higher_value_latest_ml(self):
        if self.link in LINKS_FOR_SETS_WITH_STATS:
            latest_simulation = self.setsimulatedpricestats_set.order_by('-date_simulated').first()
            if latest_simulation:
                return latest_simulation.chance_greater_opened_value_minlisting
        else:
            return None
    
    def graph_get_cgv(self):
        if self.link in LINKS_FOR_SETS_WITH_STATS:
            latest_simulation = self.setsimulatedpricestats_set.order_by('-date_simulated').first()
            if latest_simulation:
                set_code = self.code
                graph_path = f'sets-data/{set_code}/data/cgv-graph{set_code}.jpg'
                return graph_path
        return None
    
    def graph_get_mean(self):
        if self.link in LINKS_FOR_SETS_WITH_STATS:
            latest_simulation = self.setsimulatedpricestats_set.order_by('-date_simulated').first()
            if latest_simulation:
                set_code = self.code
                graph_path = f'sets-data/{set_code}/data/mean-graph{set_code}.jpg'
                return graph_path
        return None
    
    def graph_get_median(self):
        if self.link in LINKS_FOR_SETS_WITH_STATS:
            latest_simulation = self.setsimulatedpricestats_set.order_by('-date_simulated').first()
            if latest_simulation:
                set_code = self.code
                graph_path = f'sets-data/{set_code}/data/median-graph{set_code}.jpg'
                return graph_path
        return None
    
    def graph_get_gl(self):
        if self.link in LINKS_FOR_SETS_WITH_STATS:
            latest_gl_rank = self.setgainlossranking_set.order_by('-ranking_date').first()
            if latest_gl_rank:
                set_code = self.code
                graph_path = f'sets-data/{set_code}/data/gl-graph{set_code}.jpg'
                return graph_path
        return None
    
    def get_simulation_csv(self, mporml):
        mporml = str(mporml).lower()
        ok = ['mp', 'ml']
        if mporml not in ok:
            print('incorrect entry of mp or ml')
            return None
        if self.link in LINKS_FOR_SETS_WITH_STATS:
            latest_simulation = self.setsimulatedpricestats_set.order_by('-date_simulated').first()
            if latest_simulation:
                set_code = self.code
                set_data_directory = get_set_data_directory(set_code)
                print(set_data_directory)
                csv_path = f'{set_data_directory}/{mporml}{set_code}.csv'
                print(csv_path)
                return csv_path
            
class SetSimulatedPriceStats(models.Model):
    set = models.ForeignKey(Set, on_delete=models.CASCADE)
    booster_mean_marketp = models.FloatField(blank=True, null=True)
    booster_median_marketp = models.FloatField(blank=True, null=True)
    booster_gainloss_mp = models.FloatField(blank=True, null=True)
    chance_greater_opened_value_marketp = models.FloatField(max_length=5, blank=True, null=True)
    booster_mean_minlisting = models.FloatField(blank=True, null=True)
    booster_median_minlisting = models.FloatField(blank=True, null=True)
    booster_gainloss_ml = models.FloatField(blank=True, null=True)
    chance_greater_opened_value_minlisting = models.FloatField(max_length=5, blank=True, null=True)
    date_simulated = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.set.code}-{self.date_simulated}\n \
                Chance Greater (MP):%{self.chance_greater_opened_value_marketp}\n \
                Mean:{self.booster_mean_marketp}\n\
                Chance Greater MinLis: %{self.chance_greater_opened_value_minlisting}'

class SetRankings(models.Model):
    set = models.ForeignKey(Set, on_delete=models.CASCADE)
    mp_ranking = models.IntegerField(blank=True, null=True)
    ml_ranking = models.IntegerField(blank=True, null=True)
    mp_ranking_change = models.IntegerField(blank=True, null=True)
    ml_ranking_change = models.IntegerField(blank=True, null=True)
    ranking_date = models.DateField()
    # TCG Market Price
    mp_cgv_today = models.FloatField()
    mp_cgv_week = models.FloatField(blank=True, null=True)
    mp_cgv_month = models.FloatField(blank=True, null=True)
    mp_cgv_all_time = models.FloatField(default=0)
    # Minimum Listing
    ml_cgv_today = models.FloatField(blank=True, null=True)
    ml_cgv_week = models.FloatField(blank=True, null=True)
    ml_cgv_month = models.FloatField(blank=True, null=True)
    ml_cgv_all_time = models.FloatField(default=0)


    class Meta:
        unique_together = ('set', 'ranking_date')

class SetGainLossRanking(models.Model):
    set = models.ForeignKey(Set, on_delete=models.CASCADE)
    ranking_date = models.DateField()

    # Gain/Loss (gl) Ranking
    mp_gl_ranking = models.IntegerField(blank=True, null=True)
    ml_gl_ranking = models.IntegerField(blank=True, null=True)
    mp_ranking_change = models.IntegerField(blank=True, null=True)
    ml_ranking_change = models.IntegerField(blank=True, null=True)
    # Market Price
    mp_gl_today = models.FloatField(blank=True, null=True)
    mp_gl_week = models.FloatField(blank=True, null=True)
    mp_gl_month = models.FloatField(blank=True, null=True)
    mp_gl_all_time = models.FloatField(default=0)
    # Minimum Listing
    ml_gl_today = models.FloatField(blank=True, null=True)
    ml_gl_week = models.FloatField(blank=True, null=True)
    ml_gl_month = models.FloatField(blank=True, null=True)
    ml_gl_all_time = models.FloatField(default=0)


    class Meta:
        unique_together = ('set', 'ranking_date')


class SetScrapeRecord(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.timestamp}'
    
class UserSubmittedSetPriceStats(models.Model):
    set = models.ForeignKey(Set, on_delete=models.CASCADE, blank=True, null=True)
    booster_mean = models.FloatField(blank=True, null=True)
    booster_median = models.FloatField(blank=True, null=True)
    chance_greater_opened_value = models.FloatField(max_length=5, blank=True, null=True)
    date_submitted = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.set.code}-{self.date_simulated}\n \
                Chance Greater:%{self.chance_greater_opened_value}\n \
                Mean:{self.booster_mean}'
    
class UserSubmittedSetPrices(models.Model):
    set_title = models.CharField(max_length=200, blank=True, null=True)
    set_code = models.CharField(max_length=10)
    simulated_price = models.FloatField(max_length=10)

    def __str__(self):
        return f'{self.set_title} - ${self.simulated_price}'
    
    def get_simulated_price_in_pounds(self):
        return '£%.2f' %(float(self.simulated_price) / 1.27)