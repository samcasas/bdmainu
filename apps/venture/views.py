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

from .models import Venture, Branch
from .serializers import VentureSerializer, BranchSerializer
from apps.resources.helpers import Helper

class VentureView(APIView, Helper):
    permission_classes = [IsAuthenticated]
    
    def __init__(self):
        pass

    def post(self, request, *args, **kwargs):
        print('ssssss: ' + request.path)
        if 'set-venture' in request.path:
            return self.setVenture(request)
        elif 'set-image-venture' in request.path:
            return self.setVentureImage(request)
        elif 'new-branch' in request.path:
            return self.newBranch(request)
        elif 'put-branch' in request.path:
            return self.updateBranch(request)
        elif 'get-venture-information' in request.path:
            return self.getVentureInfo(request)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
            

    def get(self, request, id=None, *args, **kwargs):
        if 'get-branch' in request.path and id is not None:
            return self.getBranch(request,id)
        elif 'get-venture-information' in request.path:
            return self.getVentureInfo(request)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        
    def setVenture(self, request):
        venture_data = JSONParser().parse(request)
        venture_data['user_id'] = request.user.id
        try:
            # Intentar obtener la instancia existente de Venture para este usuario
            venture = Venture.objects.get(user_id=venture_data['user_id'])
            
            # Si existe, actualizar los campos con los datos recibidos
            serializer = VentureSerializer(venture, data=venture_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(self.responseRequest(True, 'Guardado correctamente.', serializer.data, 200), status=status.HTTP_200_OK)
            else:
                return Response(self.responseRequest(False, 'Datos no válidos.', serializer.errors, 400), status=status.HTTP_400_BAD_REQUEST)

        except Venture.DoesNotExist:
            # Si no existe, crear una nueva instancia
            serializer = VentureSerializer(data=venture_data)
            if serializer.is_valid():
                serializer.save()
                return Response(self.responseRequest(True, 'Guardado correctamente.', serializer.data, 201), status=status.HTTP_201_CREATED)
            else:
                return Response(self.responseRequest(False, 'Datos no válidos.', serializer.errors, 400), status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(self.responseRequest(False, f'No se pudo guardar. Error: {str(e)}', {}, 500), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def setVentureImage(self, request):
        # Obtener el archivo de imagen
        image_file = request.FILES.get('image')
        if not image_file:
            return Response(self.responseRequest(False, 'No se encontró ninguna imagen en la solicitud.', {}, 400), status=status.HTTP_400_BAD_REQUEST)
        
        try:
            venture = Venture.objects.get(user_id=request.user.id)
            # Subir la imagen a S3
            s3_client = boto3.client('s3',
                                     aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                     aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                                     region_name=settings.AWS_S3_REGION_NAME)
            
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            name = venture.name
            name =  name.replace(" ", "-") + f"-{venture.id}"
            file_key = f'images/logos/{request.user.id}/{name}'  # Nombre del archivo en S3
            
            # Subir el archivo a S3
            s3_client.upload_fileobj(image_file, bucket_name, file_key)
            
            # Obtener la URL de la imagen
            image_url = f'https://{bucket_name}.s3.amazonaws.com/{file_key}'
            
            # Guardar la URL en el modelo Venture
            
            venture.image = image_url
            venture.save()
            
            return Response(self.responseRequest(True, 'Actualizado correctamente.', {'image_url': image_url}, 200), status=status.HTTP_200_OK)
        
        except Venture.DoesNotExist:
            return Response(self.responseRequest(False, 'No se encontró ninguna instancia de Venture para este usuario.', {}, 404), status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response(self.responseRequest(False, f'Error al subir la imagen: {str(e)}', {}, 500), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def newBranch(self, request):
        branch_data = JSONParser().parse(request)
        user_id = request.user.id
        venture = Venture.objects.get(user_id=user_id)
        venture_id = venture.id
        try:
            branch_data['venture_id'] = venture_id
            serializer = BranchSerializer(data=branch_data)
            if serializer.is_valid():
                serializer.save()
                return Response(self.responseRequest(True, 'Sucursal creada correctamente.', serializer.data, 201), status=status.HTTP_201_CREATED)
            
            return Response(self.responseRequest(False, f'No se pudo crear la sucursal.', {}, 409), status=status.HTTP_409_CONFLICT)
        
        except Exception as e:
        
            return Response(self.responseRequest(False, f'No se pudo crear la sucursal. Error: {str(e)}', {}, 500), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def updateBranch(self, request):
        branch_data = JSONParser().parse(request)
        branch_id = branch_data.get('id')  # Asegúrate de enviar el ID de la sucursal en los datos

        if not branch_id:
            return Response(self.responseRequest(False, 'ID de la sucursal no proporcionado.', {}, 400), status=status.HTTP_400_BAD_REQUEST)

        try:
            # Obtener la sucursal existente
            branch = Branch.objects.get(id=branch_id)

            # Actualizar los datos de la sucursal
            serializer = BranchSerializer(branch, data=branch_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(self.responseRequest(True, 'Sucursal actualizada correctamente.', serializer.data, 200), status=status.HTTP_200_OK)
            else:
                return Response(self.responseRequest(False, 'Datos no válidos para la actualización.', serializer.errors, 400), status=status.HTTP_400_BAD_REQUEST)

        except Branch.DoesNotExist:
            return Response(self.responseRequest(False, 'Sucursal no encontrada.', {}, 404), status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(self.responseRequest(False, f'No se pudo actualizar la sucursal. Error: {str(e)}', {}, 500), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def getBranch(self, request, id):
        try:
            user_id = request.user.id
            venture = Venture.objects.get(user_id=user_id)
            venture_id = venture.id
            branch = Branch.objects.get(id=id, venture_id = venture_id)
            serializer = BranchSerializer(branch)
            return Response(self.responseRequest(True, f'Success', serializer.data, 200), status=200)
        except Branch.DoesNotExist:
            return Response(self.responseRequest(False, f'No se pudo encontrar la sucursal.', {}, 404), status=status.HTTP_404_NOT_FOUND)

    def getVentureInfo(self, request):
        user_id = request.user.id
        try:
            # Get venture
            venture = Venture.objects.get(user_id=user_id)
            
            # serialice venture
            venture_serializer = VentureSerializer(venture)

            # get branches
            branches = Branch.objects.filter(venture_id=venture.id)
            
            # Serialice brances
            branch_serializer = BranchSerializer(branches, many=True)

            # build response
            response_data = {
                'venture': venture_serializer.data,
                'branches': branch_serializer.data,
            }

            return Response(self.responseRequest(True, 'Información obtenida correctamente.', response_data, 200), status=status.HTTP_200_OK)

        except Venture.DoesNotExist:
            return Response(self.responseRequest(False, 'No se pudo encontrar la información de la sucursal.', {}, 404), status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(self.responseRequest(False, f'Error: {str(e)}', {}, 500), status=status.HTTP_500_INTERNAL_SERVER_ERROR)