# apps/user/views.py
import os
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
from rest_framework_simplejwt.tokens import RefreshToken
from cryptography.fernet import Fernet
from datetime import timedelta
from django.utils import timezone

#locales
from .mail import Mail
from .models import User
from .serializers import UserSerializer

class UserView(APIView):

    def __init__(self):
        # Genera una clave y la almacena de forma segura
        self.key = settings.ENCRYPTION_KEY
        self.cipher_suite = Fernet(self.key)

    def post(self, request, *args, **kwargs):
        print(request.path)
        if 'register' in request.path:
            return self.register(request)
        elif 'login' in request.path:
            return self.login(request)
        elif 'confirmation' in request.path:
            return self.confirmation(request)
        elif 'resend-verify' in request.path:
            return self.resend_confirmation(request)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        return self.update(request)

    def register(self, request):
        user_data = JSONParser().parse(request)
        try:
            user = User.objects.get(email=user_data['email'])
            return Response(self.responseRequest(False, 'Ya existe una cuenta con este correo.', [], 409), status=status.HTTP_409_CONFLICT)
        except User.DoesNotExist:

        # Encriptar la contraseña antes de guardarla
            user_data['password'] = make_password(user_data['password'])
            #Generamos un token para encriptarlo
            user_data['token'] = os.urandom(30).hex()
            expiration_date = timezone.now() + timedelta(hours=4)
            user_data['tokenExpirationDate'] = expiration_date
            serializer = UserSerializer(data=user_data)
            if serializer.is_valid():
                user = serializer.save()  # Guardar el usuario y obtener la instancia del usuario
                token = str(user.token).encode('utf-8')  # Convertir el id a bytes
                encrypted_id = self.cipher_suite.encrypt(token)  # Encriptar el id del usuario
                #Guardamos el token encriptado
                user_data['token'] = encrypted_id.decode('utf-8') 
                mail = Mail()
                mail.send_confirmation_mail(request, user_data)
                return Response(self.responseRequest(True, 'Agregado correctamente.', serializer.data, 201), status=status.HTTP_201_CREATED)
            return Response(self.responseRequest(False, 'Ocurrió un error, revisa tus datos...', serializer.data, 400), status=status.HTTP_400_BAD_REQUEST)
    
    def resend_confirmation(self, request):
        
        try:
            user_data = JSONParser().parse(request)
            user = User.objects.get(email=user_data['email'])
            expiration_date = timezone.now() + timedelta(hours=4)
                    
            user.token = os.urandom(30).hex()
            user.tokenExpirationDate = expiration_date
            user.save()

            token = str(user.token).encode('utf-8')
            encrypted_id = self.cipher_suite.encrypt(token)
                    
            user_data['token'] = encrypted_id.decode('utf-8')
            user_data['name'] = user.name

            mail = Mail()
            mail.send_confirmation_mail(request, user_data)

            user_serializer = UserSerializer(user)

            return Response(self.responseRequest(True, 'Enviado correctamente.', user_serializer.data, 200), status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(self.responseRequest(False, 'Usuario no encontrado.', [], 404), status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(self.responseRequest(False, f'No se pudo enviar el correo. Error: {str(e)}', {}, 500), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def confirmation(self, request):
        token = request.data.get('token')  # Obtener el token encriptado desde la solicitud
        try:
            
            # Decodificar el token encriptado a bytes
            token_bytes = token.encode('utf-8')
            # Desencriptar el token
            token_decrypt = self.cipher_suite.decrypt(token_bytes)
            # Convertir el token desencriptado a cadena
            token_decrypt_str = token_decrypt.decode('utf-8')

            user = User.objects.get(token=token_decrypt_str)
            user_serializer = UserSerializer(user)
            if user.tokenExpirationDate and user.tokenExpirationDate < timezone.now():
                return Response(self.responseRequest(False, 'El token ha expirado.', user_serializer.data, 200), status=status.HTTP_200_OK)
            
            user.status = User.TOUR 
            user.save()

            return Response(self.responseRequest(True, 'Agregado correctamente.', token_decrypt_str, 200),status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(self.responseRequest(False, 'El token ha expirado.', token_decrypt_str, 200), status=status.HTTP_200_OK)
        except Exception as e:
            # Manejar cualquier error de desencriptación
            return Response(self.responseRequest(False, 'No se pudo desencriptar el token.', {}, 400), status=status.HTTP_400_BAD_REQUEST)
    
    def login(self, request):
        username = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
           
            if user.status == User.NEW:
                self.resend_confirmation(request)
                return Response(self.responseRequest(False, "La cuenta no ha sido verificada.", {}, 403), status=status.HTTP_403_FORBIDDEN)
            

            refresh = RefreshToken.for_user(user)
            login(request, user)
            response =  {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(self.responseRequest(True, 'Las credenciales son validas.', response, 200), status=status.HTTP_200_OK)
        return Response(self.responseRequest(False, "El correo electrónico o la contraseña no son correctos.", {}, 401), status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def responseRequest(self, status, msg, data, success):
        return {'success': success, 'message': msg,'data': data, 'status' : status }

