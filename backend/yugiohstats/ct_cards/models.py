from django.db import models
from ct_expansions.models import Expansion
from datetime import date, timedelta

# Create your models here.
class CardBlueprint(models.Model):
    id = models.IntegerField(primary_key=True)
    expansion = models.ForeignKey(Expansion, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    
    yugioh_rarity = models.CharField(max_length=100)
    collector_number = models.CharField(max_length=10)
    first_ed = models.BooleanField(blank=True, null=True)

    img_download_link = models.CharField(max_length=500, blank=True, null=True)

    def get_price(self):
        # Get the latest price history record
        latest_price = self.cardpricehistory_set.order_by('-date').first()
        
        # If there is no price history, return None
        if not latest_price:
            return None
        
        # Return the first non-null price
        return latest_price.min_price_gbp or latest_price.unlim_min_price_gbp or None
    
    
    def get_price_yday(self):
        today = date.today()
        yday = today - timedelta(days=1)
        # Get the latest price history record
        latest_price = self.cardpricehistory_set.filter(date=yday).first()
        
        # If there is no price history, return None
        if not latest_price:
            return None
        
        # Return the first non-null price
        return latest_price.min_price_gbp or latest_price.unlim_min_price_gbp or None

    def __str__(self):
        return f'{self.expansion.code}-en{self.collector_number} - {self.name}'
    
class CardPriceHistory(models.Model):
    card = models.ForeignKey(CardBlueprint, on_delete=models.CASCADE)
    date = models.DateField()

    min_price_gbp = models.FloatField(blank=True, null=True)
    min_price_gbp_formatted = models.CharField(max_length=12, blank=True, null=True)
    
    unlim_min_price_gbp = models.FloatField(blank=True, null=True)
    unlim_min_price_gbp_formatted = models.CharField(max_length=12, blank=True, null=True)

    class Meta:
        unique_together = ('card', 'date')

    def __str__(self):
        return f'{self.card.name} - {self.min_price_gbp_formatted} - {self.date}'