from django.urls import path

from .views import (set_list_view, set_detail_view,
                    new_set_list_view, set_detail_graph_view)

urlpatterns = [
    path('', new_set_list_view, name='set-list'),
    path('<int:id>/', set_detail_view, name='set-detail'),
    path('<int:id>/graphs/', set_detail_graph_view, name='set-detail-graphs'),
]
