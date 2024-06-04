from django.shortcuts import render
from django.forms.models import model_to_dict

from rest_framework.decorators import api_view
from rest_framework.response import Response

from sets.models import Set
from sets.serializers import SetSerializer, UserSubmittedSetPricesSerializer

@api_view(['POST'])
def api_home(request, *args, **kwargs):
    # instance = Set.objects.all().first()
    serializer = UserSubmittedSetPricesSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        # instance = serializer.save()
        print(serializer.data)
        return Response(serializer.data)
    return Response()