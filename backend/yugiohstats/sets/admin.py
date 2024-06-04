from django.contrib import admin
from .models import Set, UserSubmittedSetPrices

class SetAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'link',
        'average_price',
        'code'
    ]

admin.site.register(Set, SetAdmin)

class UserSubmittedSetPricesAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'set_code',
        'set_title',
        'simulated_price'
    ]
admin.site.register(UserSubmittedSetPrices, UserSubmittedSetPricesAdmin)