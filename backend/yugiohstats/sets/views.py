from django.shortcuts import render
from django.db.models import Count
from datetime import date
from rest_framework import generics

from cards.models import Card

from helpers.stats import get_user_cgv_gainloss
from helpers.utils import pct_str

from .forms import UserSubmittedBoosterPriceForm
from .models import Set, UserSubmittedSetPrices, SetRankings, SetGainLossRanking
from .serializers import SetSerializer, SetSimulatedPriceStats

class SetDetailApiView(generics.RetrieveAPIView):
    queryset = Set.objects.all()
    serializer_class = SetSerializer
    # lookup_field = 'pk'

def new_set_list_view(request):
    rank_by = request.GET.get('rank_by', 'cgv')
    sort = request.GET.get('sort', 'mp_ranking')
    order = request.GET.get('order', 'asc')
    mporml = request.GET.get('mporml', 'mp')
    if order == 'desc':
        sort = '-' + sort
    context = {
        'rank_by': rank_by,
        'mporml': mporml,
        'current_sort': sort.lstrip('-'),
        'current_order': order,
    }
    if rank_by == 'cgv':
        rankings = SetRankings.objects.filter(ranking_date=date.today()).order_by(sort)
        context['rankings'] = rankings
    if rank_by == 'gl':
       gl_rankings = SetGainLossRanking.objects.filter(ranking_date=date.today()).order_by(sort)
       context['gl_rankings'] = gl_rankings
    return render(request, 'rankings-index.html', context)


def old_new_set_list_view(request):
    mp_rankings = SetRankings.objects.filter(ranking_date=date.today()).order_by('mp_ranking')
    context = {
        'rankings': mp_rankings
    }
    return render(request, 'rankings-index.html', context)

def set_list_view(request):
    booster_qs = Set.objects.filter(type='Booster')
    premium_qs = Set.objects.filter(type='Premium Pack')
    champion_qs = Set.objects.filter(type='Champion Pack')
    tournament_qs = Set.objects.filter(type='Tournament Pack')
    context = {
        'booster_list': booster_qs,
        'premium_list': premium_qs,
        'champion_list': champion_qs,
        'tournament_list': tournament_qs,
    }
    return render(request, 'index.html', context)

def old_set_detail_view(request, id):
    set_instance = Set.objects.get(id=id)
    card_qs = Card.objects.filter(set=set_instance)
    form = UserSubmittedBoosterPriceForm(request.POST or None)
    
    # Get the sorting option from the request
    sort_by = request.GET.get('sort_by')
    
    # Apply sorting based on the selected option
    if sort_by == 'name':
        card_qs = card_qs.order_by('card_name')
    elif sort_by == 'code':
        card_qs = card_qs.order_by('card_code')
    elif sort_by == 'price_low':
        card_qs = card_qs.order_by('tcg_market_price')
    elif sort_by == 'price_high':
        card_qs = card_qs.order_by('-tcg_market_price')

    # Fetch rarity options and counts for the set
    rarity_options = card_qs.values('card_rarity').annotate(count=Count('card_rarity'))

    # Check if any rarity filter is applied
    selected_rarities = request.POST.getlist('rarity')

    # If rarity filters are selected, filter cards accordingly
    if selected_rarities:
        card_qs = card_qs.filter(card_rarity__in=selected_rarities)

    cards_count = card_qs.count()
    context = {
        'set': set_instance,
        'form': form,
        'card_list': card_qs,
        'card_count': cards_count,
        'rarity_options': rarity_options,
        'selected_rarities': selected_rarities,
        'submitted': False

    }
    
    if form.is_valid():
        cleaned_data = form.cleaned_data
        price = cleaned_data['price']
        print(price)
        set_code = set_instance.code
        dict_cgv_gl = get_user_cgv_gainloss(set_code, price )
        mp_cgv = dict_cgv_gl[0]['mp-cgv']
        ml_cgv = dict_cgv_gl[1]['ml-cgv']
        print(mp_cgv, ml_cgv)
        mp_gl = dict_cgv_gl[0]['mp-gainloss']
        ml_gl = dict_cgv_gl[1]['ml-gainloss']
        
        print(mp_gl, ml_gl)
        user_gl = {'mp': mp_gl,
                   'ml': ml_gl}
        user_cgv = {'mp': mp_cgv,
                   'ml': ml_cgv}
        context['submitted'] = True
        context['user_gl'] = user_gl
        context['user_cgv'] = user_cgv
        context['user_price'] = '$%.2f' % price
        return render(request, 'sets/set-detail.html', context)
    return render(request, 'sets/set-detail.html', context)

def set_detail_view(request, code):
    set_code = str(code).upper()
    set_instance = Set.objects.get(code=set_code)
    card_qs = Card.objects.filter(set=set_instance)
    form = UserSubmittedBoosterPriceForm(request.POST or None)
    
    # Get the sorting option from the request
    sort_by = request.GET.get('sort_by')
    
    # Apply sorting based on the selected option
    if sort_by == 'name':
        card_qs = card_qs.order_by('card_name')
    elif sort_by == 'code':
        card_qs = card_qs.order_by('card_code')
    elif sort_by == 'price_low':
        card_qs = card_qs.order_by('tcg_market_price')
    elif sort_by == 'price_high':
        card_qs = card_qs.order_by('-tcg_market_price')

    # Fetch rarity options and counts for the set
    rarity_options = card_qs.values('card_rarity').annotate(count=Count('card_rarity'))

    # Check if any rarity filter is applied
    selected_rarities = request.POST.getlist('rarity')

    # If rarity filters are selected, filter cards accordingly
    if selected_rarities:
        card_qs = card_qs.filter(card_rarity__in=selected_rarities)

    cards_count = card_qs.count()
    context = {
        'set': set_instance,
        'form': form,
        'card_list': card_qs,
        'card_count': cards_count,
        'rarity_options': rarity_options,
        'selected_rarities': selected_rarities,
        'submitted': False

    }
    
    if form.is_valid():
        cleaned_data = form.cleaned_data
        price = cleaned_data['price']
        print(price)
        set_code = set_instance.code
        dict_cgv_gl = get_user_cgv_gainloss(set_code, price )
        mp_cgv = dict_cgv_gl[0]['mp-cgv']
        ml_cgv = dict_cgv_gl[1]['ml-cgv']
        print(mp_cgv, ml_cgv)
        mp_gl = dict_cgv_gl[0]['mp-gainloss']
        ml_gl = dict_cgv_gl[1]['ml-gainloss']
        
        print(mp_gl, ml_gl)
        user_gl = {'mp': mp_gl,
                   'ml': ml_gl}
        user_cgv = {'mp': mp_cgv,
                   'ml': ml_cgv}
        context['submitted'] = True
        context['user_gl'] = user_gl
        context['user_cgv'] = user_cgv
        context['user_price'] = '$%.2f' % price
        return render(request, 'sets/set-detail.html', context)
    return render(request, 'sets/set-detail.html', context)

def set_detail_graph_view(request, id):
    set_instance = Set.objects.get(id=id)
    gl_graph = set_instance.graph_get_gl()
    cgv_graph = set_instance.graph_get_cgv()
    mean_graph = set_instance.graph_get_mean()
    median_graph = set_instance.graph_get_median()
    context = {'set': set_instance,}
    if gl_graph != None:
        context['gl_graph'] = gl_graph
    if cgv_graph != None:
        context['cgv_graph'] = cgv_graph
    if mean_graph != None:
        context['mean_graph'] = mean_graph
    if median_graph != None:
        context['median_graph'] = median_graph
    return render(request, 'sets/set-detail-graphs.html', context)
