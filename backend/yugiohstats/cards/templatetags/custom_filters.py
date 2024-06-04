
from django import template

register = template.Library()

@register.filter
def format_rarity(rarity):
    return ' '.join(rarity.split('-'))
