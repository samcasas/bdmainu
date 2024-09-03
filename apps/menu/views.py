import os
import boto3
from django.conf import settings
from django.utils.http import urlencode
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser

from .models import Category, Product, Promotion
from .serializers import VentureSerializer, BranchSerializer, BranchImageSerializer
from apps.resources.helpers import Helper

class MenuView(APIView, Helper):
    action = None
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.action = kwargs.get('action')

    def post(self, request, *args, **kwargs):
        if self.action == 'add_category':
            return self.addCategory(request)
        elif self.action == 'add_product':
            return self.addProduct(request)
        elif self.action == 'add_promotion':
            return self.addPromotion(request)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id=None, *args, **kwargs):
        pass

    def delete(self, request, id=None, *args, **kwargs):
        pass


    def addCategory(self, request):
        pass

    def addProduct(self, request):
        pass

    def addPromotion(self, request):
        pass