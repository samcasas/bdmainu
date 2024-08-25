import os
from django.conf import settings
from django.utils.http import urlencode
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Country, State
from .serializers import CountrySerializer, StateSerializer
from .helpers import Helper

class ResourcesView(APIView, Helper):
    permission_classes = [IsAuthenticated]
    
    def __init__(self):
        pass

    def get(self, request, *args, **kwargs):
        print(request.path)
        if 'countries' in request.path:
            return self.getCountries()
        elif 'states' in request.path:
            return self.getStates(request)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)



    def getCountries(self):
        countries = Country.objects.all()
        serializer = CountrySerializer(countries, many=True)
        return Response(self.responseRequest(True, "Success", serializer.data, 200), status=status.HTTP_200_OK)



    def getStates(self, request):
        country_id =  request.query_params.get('country_id')
        states = State.objects.filter(country = country_id)
        serializer = StateSerializer(states, many=True)
        return Response(self.responseRequest(True, "Success", serializer.data, 200), status=status.HTTP_200_OK)