from django.db import models
from ct_games.models import Game

# Create your models here.
class Expansion(models.Model):
    id = models.IntegerField(primary_key=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    code = models.CharField(max_length=12)
    name = models.CharField(max_length=150)

    is_booster_box = models.BooleanField(blank=True, null=True)
    bb_blueprint_id = models.IntegerField(blank=True, null=True)
    min_price_gbp = models.FloatField(blank=True, null=True)
    min_price_gbp_formatted = models.CharField(max_length=12, blank=True, null=True)


    def __str__(self):
        return f'{self.code} - {self.name}'
    
class ExpSimulatedPriceStats(models.Model):
    expansion = models.ForeignKey(Expansion, on_delete=models.CASCADE)
    date_simulated = models.DateField(blank=True, null=True)
    mean = models.FloatField(blank=True, null=True)
    median = models.FloatField(blank=True, null=True)
    gainloss = models.FloatField(blank=True, null=True)
    cgv = models.FloatField(max_length=5, blank=True, null=True)
   
    def __str__(self):
        return f'{self.expansion.code}-{self.date_simulated},CGV:%{self.cgv}, Mean:{self.mean}'
    
class ExpRankings(models.Model):

    expansion = models.ForeignKey(Expansion, on_delete=models.CASCADE)
    ranking_date = models.DateField()

    cgv_ranking = models.IntegerField(blank=True, null=True)
    cgv_ranking_change = models.IntegerField(blank=True, null=True)

    cgv_today = models.FloatField(blank=True, null=True)
    cgv_week = models.FloatField(blank=True, null=True)
    cgv_month = models.FloatField(blank=True, null=True)
    cgv_all_time = models.FloatField(blank=True, null=True)

    gl_ranking = models.IntegerField(blank=True, null=True)
    gl_ranking_change = models.IntegerField(blank=True, null=True)
    gl_today = models.FloatField(blank=True, null=True)
    gl_week = models.FloatField(blank=True, null=True)
    gl_month = models.FloatField(blank=True, null=True)
    gl_all_time = models.FloatField(blank=True, null=True)

    class Meta:
        unique_together = ('expansion', 'ranking_date')
