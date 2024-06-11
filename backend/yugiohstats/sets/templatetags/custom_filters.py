from django import template

register = template.Library()

@register.filter
def format_pct(pct):
    if pct == None:
        return 'N/A'
    pct = '%.2f' %(pct)
    return pct + '%'

@register.filter
def format_dollars(price):
    if price == None:
        return 'N/A'
    elif price == 0:
        return '$%.2f' %(price)
    elif price > 0:
        return '+$%.2f' %(price)
    elif price < 0:
        abs_price = abs(price)
        return '-$%.2f' %(abs_price)
    else:
        return 'Error'
    
@register.filter
def format_sterling(price):
    if price == None:
        return 'N/A'
    price = float(price)
    if price == 0:
        return '£%.2f' %(price)
    elif price > 0:
        return '+£%.2f' %(price)
    elif price < 0:
        abs_price = abs(price)
        return '-£%.2f' %(abs_price)
    else:
        return 'Error'

@register.filter
def format_rarity(rarity):
    return ' '.join(rarity.split('-'))

@register.filter
def format_pct_change(pct):
    if pct == None:
        return 'N/A'
    pct = '%.2f' %(pct)
    if '-' in pct or pct == '0.00':
        return pct + '%'
    else:
        return f'+{pct}%'

@register.filter
def format_ranking_change(rank_change):
    if rank_change is None:
        return 'N/A'
    if (rank_change == 0):
        return f'={rank_change}'
    if (rank_change < 0):
        return str(rank_change)
    else:
        return f'+{rank_change}'
    
@register.filter
def pn_cgv(cgv):
    return 'positive' if cgv > 50 else 'negative'

@register.filter
def pn_change(pct):
    if pct is None:
        return None
    if pct > 0:
        return 'positive'
    if pct < 0:
        return 'negative'
    if pct == 0:
        return 'zero'

