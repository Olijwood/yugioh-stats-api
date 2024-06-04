from rest_framework import generics

from api.mixins import StaffEditorPermissionMixin

from .models import Set, UserSubmittedSetPrices, SetRankings
from .serializers import (SetSerializer, MPSetRankingsSerializer,
                          UserSubmittedSetPricesSerializer,
                          UserSubmittedSetPricesDetailSerializer,
                          MLSetRankingsSerializer)
from helpers.validators import get_set_code_title_dict

from datetime import date

SET_CODES_DICT = get_set_code_title_dict()

class SetListAPIView(
        StaffEditorPermissionMixin,
        generics.ListAPIView
    ):
    queryset = Set.objects.all()
    serializer_class = SetSerializer

set_list_api_view = SetListAPIView.as_view()

class SetDetailApiView(
        StaffEditorPermissionMixin,
        generics.RetrieveAPIView
    ):
    queryset = Set.objects.all()
    serializer_class = SetSerializer
    # lookup_field = 'pk'

set_detail_view = SetDetailApiView.as_view()

class SetRankingMPTodayListAPIView(
    StaffEditorPermissionMixin,
    generics.ListAPIView,
):
    queryset = SetRankings.objects.filter(ranking_date=date.today()).order_by('mp_ranking')
    serializer_class = MPSetRankingsSerializer

set_ranking_mp_list_view = SetRankingMPTodayListAPIView.as_view()

class SetRankingMLTodayListAPIView(
    StaffEditorPermissionMixin,
    generics.ListAPIView,
):
    queryset = SetRankings.objects.filter(ranking_date=date.today()).order_by('ml_ranking')
    serializer_class = MLSetRankingsSerializer

set_ranking_ml_list_view = SetRankingMLTodayListAPIView.as_view()

# 'User Submitted Set Prices' == 'USSP'

class UserSubmittedSetPricesListCreateAPIView(
        StaffEditorPermissionMixin,
        generics.ListCreateAPIView
    ):
    queryset = UserSubmittedSetPrices.objects.all()
    serializer_class = UserSubmittedSetPricesSerializer

    def perform_create(self, serializer):
        #serializer.save(user=self.request.user)
        print(serializer.validated_data)
        set_code = str(serializer.validated_data.get('set_code')).upper()
        title = serializer.validated_data.get('set_title') or None
        if title is None:

            title = SET_CODES_DICT[set_code]
        serializer.save(set_title=title)

ussp_list_create_view = UserSubmittedSetPricesListCreateAPIView.as_view()


class USSPDetailApiView(
        StaffEditorPermissionMixin,
        generics.RetrieveAPIView
    ):
    queryset = UserSubmittedSetPrices.objects.all()
    serializer_class = UserSubmittedSetPricesDetailSerializer
    # lookup_field = 'pk'

ussp_detail_view = USSPDetailApiView.as_view()

class USSPUpdateApiView(
        StaffEditorPermissionMixin,
        generics.RetrieveAPIView,
        generics.UpdateAPIView
    ):
    queryset = UserSubmittedSetPrices.objects.all()
    serializer_class = UserSubmittedSetPricesSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        print(serializer)
        set_code =  str(serializer.validated_data.get('set_code')).upper()
        instance = serializer.save(set_code=set_code)
        # set_code = str(instance.set_code).upper()
        if not instance.set_title:
            instance.set_title = SET_CODES_DICT[set_code]

ussp_update_view = USSPUpdateApiView.as_view()

class USSPDeleteApiView(
        StaffEditorPermissionMixin,
        generics.DestroyAPIView
        ):
    queryset = UserSubmittedSetPrices.objects.all()
    serializer_class = UserSubmittedSetPricesSerializer
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        # isntance
        super().perform_destroy(instance)

ussp_delete_view = USSPDeleteApiView.as_view()

