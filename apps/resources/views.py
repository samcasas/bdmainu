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

from .models import Country, State, City
from .serializers import CountrySerializer, StateSerializer, CitySerializer
from .helpers import Helper

class ResourcesView(APIView, Helper):
    permission_classes = [IsAuthenticated]
    
    def __init__(self):
        pass

    def get(self, request, *args, **kwargs):
        print(request.path)
        if 'get-countries' in request.path:
            return self.getCountries()
        elif 'get-states' in request.path:
            return self.getStates(request)
        elif 'get-cities' in request.path:
            return self.getCities(request)
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
    

    def getCities(self, request):
        state_code = request.query_params.get('state_code')
        print(state_code)
        cities = City.objects.filter(state_code = state_code)
        
        serializer = CitySerializer(cities, many=True)
        return Response(self.responseRequest(True, "Success", serializer.data, 200), status=status.HTTP_200_OK)