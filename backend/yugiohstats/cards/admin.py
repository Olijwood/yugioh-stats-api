from django.contrib import admin

from .models import Card, CardImage

class CardAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'card_code',
        'card_name',
        #'tcg_market_price',
        'card_rarity',
    ]

admin.site.register(Card, CardAdmin)
admin.site.register(CardImage)