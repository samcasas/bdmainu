from rest_framework import serializers
from .models import Country, State

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country_id', 'name', 'emoji']

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'

