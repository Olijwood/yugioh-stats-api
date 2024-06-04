from django.urls import path, include

from rest_framework.authtoken.views import obtain_auth_token

from .views import (api_home,
                    )

urlpatterns = [
    path('auth/', obtain_auth_token),
    path('', api_home, name='api-home'),
    path('sets/', include('sets.api_urls'), name='set-api-urls'),
]
