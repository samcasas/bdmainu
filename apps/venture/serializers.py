from rest_framework import serializers
from .models import Venture, Branch

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'

class VentureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venture
        fields = '__all__'

