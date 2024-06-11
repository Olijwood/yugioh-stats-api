from django.urls import path

from .views import expansion_rank_view

urlpatterns = [
    path('<int:game_id>/expansions/', expansion_rank_view, name='expansion-rank')
]
