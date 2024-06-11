from datetime import date
from django.shortcuts import render

from .models import ExpRankings

def index_yugioh_expansion_rank_view(request):
    rank_by = request.GET.get('rank_by', 'cgv')
    sort = request.GET.get('sort', 'cgv_ranking')
    order = request.GET.get('order', 'asc')
    if order == 'desc':
        sort = '-' + sort
    rankings = ExpRankings.objects.filter(expansion__game__id=4).filter(ranking_date=date.today()).order_by(sort)
    context = {
        'rank_by': rank_by,
        'current_sort': sort.lstrip('-'),
        'current_order': order,
        'rankings': rankings
    }
    return render(request, 'rankings-ct-index.html', context)

def expansion_rank_view(request, game_id=4):
    # game = request.GET.get('game', '4')
    rank_by = request.GET.get('rank_by', 'cgv')
    sort = request.GET.get('sort', 'cgv_ranking')
    order = request.GET.get('order', 'asc')
    if order == 'desc':
        sort = '-' + sort
    rankings = ExpRankings.objects.filter(expansion__game__id=game_id).filter(ranking_date=date.today())
    context = {
        'rank_by': rank_by,
        'current_sort': sort.lstrip('-'),
        'current_order': order,
        'rankings': rankings
    }
    return render(request, 'rankings-ct-index.html', context)
