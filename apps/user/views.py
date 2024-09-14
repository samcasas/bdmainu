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
from apps.menu.models import Category
from apps.venture.models import Venture, Branch
from apps.menu.serializers import CategorySerializer
from .serializers import UserSerializer
from apps.resources.helpers import Helper

class AuthView(APIView, Helper):

    def __init__(self):
        # Genera una clave y la almacena de forma segura
        self.key = settings.ENCRYPTION_KEY
        self.cipher_suite = Fernet(self.key)

    def post(self, request, *args, **kwargs):
        
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
            userAuth = User.objects.get(email=username)
            response =  {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'name': userAuth.name,
                'status': userAuth.status,
                'image': userAuth.image
            }
            return Response(self.responseRequest(True, 'Las credenciales son validas.', response, 200), status=status.HTTP_200_OK)
        return Response(self.responseRequest(False, "El correo electrónico o la contraseña no son correctos.", {}, 401), status=status.HTTP_401_UNAUTHORIZED)

class UserView(APIView, Helper):
    action = None
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.action = kwargs.get('action')

    def post(self, request, *args, **kwargs):
        #categories
        if self.action == 'update_user':
            return self.updateUser(request)
        elif self.action == 'upload_image_profile':
            return self.uploadImageProfile(request)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id=None, *args, **kwargs):
        if self.action == 'get_profile_data':
            return self.getProfileData(request)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def updateUser(self, request):
        user_id = request.user.id 
        user_data = request.data   

        try:
            user = User.objects.get(id=user_id) 
            serializer = UserSerializer(user, data=user_data, partial=True)  # partial=True para actualizaciones parciales
            
            if serializer.is_valid():
                
                serializer.save()
                return Response(self.responseRequest(True, 'Usuario actualizado correctamente.', serializer.data, 200), status=status.HTTP_200_OK)
            else:
                return Response(self.responseRequest(False, 'Datos inválidos.', serializer.errors, 409), status=status.HTTP_409_CONFLICT)
        
        except User.DoesNotExist:
            return Response(self.responseRequest(False, 'No se encontró el usuario.', {}, 404), status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(self.responseRequest(False, f'Error al actualizar el usuario: {str(e)}', {}, 500), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
    def uploadImageProfile(self, request):
        # Obtener el archivo de imagen
        image_file = request.FILES.get('image')
        user_id = request.user.id

        if not image_file:
            return Response(self.responseRequest(False, 'No se encontró ninguna imagen en la solicitud.', {}, 400), status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
            # Subir la imagen a S3
            s3_client = self.getS3Client()
            
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            name = user.name
            name =  name.lower().replace(" ", "-")
            file_key = f'images/profile/{name}-{user_id}'  # Nombre del archivo en S3
            
            # Eliminar la imagen anterior si existe
            if user.image:
                # Extraer la clave del archivo anterior desde la URL almacenada
                old_file_key = user.image.split(f'https://{bucket_name}.s3.amazonaws.com/')[1]
                s3_client.delete_object(Bucket=bucket_name, Key=old_file_key)

            # Subir el archivo a S3
            s3_client.upload_fileobj(image_file, bucket_name, file_key)
            
            # Obtener la URL de la imagen
            image_url = f'https://{bucket_name}.s3.amazonaws.com/{file_key}'
            
            # Guardar la URL en el modelo Venture
            
            user.image = image_url
            user.save()
            
            return Response(self.responseRequest(True, 'Actualizado correctamente.', {'image_url': image_url}, 200), status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response(self.responseRequest(False, 'No se encontró ninguna instancia de User para este usuario.', {}, 404), status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response(self.responseRequest(False, f'Error al subir la imagen: {str(e)}', {}, 500), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


    def getProfileData(self, request):
        try:
            user_id = request.user.id
            
            # Obtén los datos del usuario
            user = User.objects.get(id=user_id)
            
            # Obtén las primeras cuatro categorías con más clics
            categories = Category.objects.filter(user_id=user_id).order_by('-clicks')[:4]
            venture = Venture.objects.get(user_id=user_id)
            branches_count = Branch.objects.filter(venture_id = venture.id).count()
            category_serializer = CategorySerializer(categories, many=True)
            
            # Estructura la respuesta
            response_data = {
                    'user': {
                        "name": user.name,
                        "email": user.email,
                        "image": user.image
                    },
                    'categories': category_serializer.data,
                    'venture': {
                        "id": venture.id,
                        "name": venture.name,
                        "branches_count": branches_count
                    },
                    "subscription":{
                        "name": "Estándar",
                        "expired": "25/11/2024"
                    }
                
            }
            
            return Response(self.responseRequest(False, 'UUsuario encontrado.', response_data, 200), status=status.HTTP_200_OK)
            
        except User.DoesNotExist:
            return Response(self.responseRequest(False, 'No se pudo encontrar el usuario.', {}, 404), status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response(self.responseRequest(False, str(e), {}, 500), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        

