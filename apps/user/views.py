# apps/user/views.py
from django.conf import settings
from django.utils.http import urlencode
from django.contrib.auth import authenticate, login
from rest_framework.parsers import JSONParser
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .mail import Mail
from .models import User
from .serializers import UserSerializer

class UserView(APIView):

    def post(self, request, *args, **kwargs):
        if 'register' in request.path:
            return self.register(request)
        elif 'login' in request.path:
            return self.login(request)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        return self.update(request)

    def register(self, request):
        user_data = JSONParser().parse(request)
        # Encriptar la contraseña antes de guardarla
        user_data['password'] = make_password(user_data['password'])
        serializer = UserSerializer(data=user_data)
        if serializer.is_valid():
            serializer.save()
            mail = Mail()
            mail.send_confirmation_mail(request, user_data)
            return Response(self.responseRequest(True, 'Agregado correctamente.', serializer.data), status=status.HTTP_201_CREATED)
        return Response(self.responseRequest(False, 'Ocurrió un error, revisa tus datos..', serializer.data), status=status.HTTP_400_BAD_REQUEST)

    def login(self, request):
        username = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def responseRequest(self, status, msg, data):
        return {'success': status, 'message': msg,'data': data }

