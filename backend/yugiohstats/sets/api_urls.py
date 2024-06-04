from django.urls import path

from .api_views import (set_detail_view, set_list_api_view,
                        ussp_detail_view, ussp_update_view,
                        ussp_list_create_view, ussp_delete_view, 
                        set_ranking_mp_list_view, set_ranking_ml_list_view)

urlpatterns = [
    # sets
    path('', set_list_api_view, name='set-list-api'),
    path('<int:pk>/', set_detail_view, name='set-detail-api'),
    path('ranking/mp/', set_ranking_mp_list_view, name='mp-ranking-list-api'),
    path('ranking/ml/', set_ranking_ml_list_view, name='mlranking-list-api'),

    # USSP (user submitted set prices)
    path('ussp/', ussp_list_create_view, name='ussp-list-create-api'),
    path('ussp/<int:pk>/update/', ussp_update_view, name='ussp-update-api'),
    path('ussp/<int:pk>/delete/', ussp_delete_view, name='ussp-delete-api'),
    path('ussp/<int:pk>/', ussp_detail_view, name='ussp-detail-api')
]

