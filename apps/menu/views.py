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
from .serializers import CategorySerializer, ProductSerializer, PromotionSerializer
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
        elif self.action == 'update_category':
            return self.updateCategory(request)
        elif self.action == 'add_product':
            return self.addProduct(request)
        elif self.action == 'add_promotion':
            return self.addPromotion(request)
        elif self.action == 'upload_image_category':
            return self.uploadImageCategory(request)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id=None, *args, **kwargs):
        if self.action == 'get_categories':
            return self.getCategories(request)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id=None, *args, **kwargs):
        if self.action == 'delete_category' and id is not None:
            return self.deleteCategory(request, id)
        elif self.action == 'delete_promotion' and id is not None:
            return self.deletePromotion(request, id)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def addCategory(self, request):
        category_data = JSONParser().parse(request)
        user_id = request.user.id
        try:
            category_data['user_id'] = user_id
            category_data['image'] = ""
            category_data['status'] = category_data['status'] = 1 if category_data['status'] == True else 0
            serializer = CategorySerializer(data=category_data)
            if serializer.is_valid():
                serializer.save()
                return Response(self.responseRequest(True, 'Categoría creada correctamente.', serializer.data, 201), status=status.HTTP_201_CREATED)
            
            return Response(self.responseRequest(False, f'No se pudo crear la categoría.', {}, 409), status=status.HTTP_409_CONFLICT)
        
        except Exception as e:
        
            return Response(self.responseRequest(False, f'No se pudo crear la categoría. Error: {str(e)}', {}, 500), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def updateCategory(self, request):
        category_data = JSONParser().parse(request)
        user_id = request.user.id
        try:
            category = Category.objects.get(id=category_data['id'])
            category_data['user_id'] = user_id
            category_data['status'] = 1 if category_data['status'] == True else 0
            serializer = CategorySerializer(category, data=category_data)
            if serializer.is_valid():
                serializer.save()
                return Response(self.responseRequest(True, 'Categoría actualizada correctamente.', serializer.data, 200), status=status.HTTP_200_OK)
            
            return Response(self.responseRequest(False, 'No se pudo actualizar la categoría.', serializer.errors, 409), status=status.HTTP_409_CONFLICT)
        
        except Category.DoesNotExist:
            return Response(self.responseRequest(False, 'Categoría no encontrada.', {}, 404), status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response(self.responseRequest(False, f'No se pudo actualizar la categoría. Error: {str(e)}', {}, 500), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def uploadImageCategory(self, request):
        # Obtener el archivo de imagen
        image_file = request.FILES.get('image')
        category_id = request.data.get('category_id')

        if not image_file:
            return Response(self.responseRequest(False, 'No se encontró ninguna imagen en la solicitud.', {}, 400), status=status.HTTP_400_BAD_REQUEST)
        
        try:
            category = Category.objects.get(id=category_id)
            # Subir la imagen a S3
            s3_client = self.getS3Client()
            
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            name = category.name
            name =  name.lower().replace(" ", "-") + f"-{category.id}"
            file_key = f'images/categories/{request.user.id}/{name}'  # Nombre del archivo en S3
            
            # Eliminar la imagen anterior si existe
            if category.image != "":
                # Extraer la clave del archivo anterior desde la URL almacenada
                old_file_key = category.image.split(f'https://{bucket_name}.s3.amazonaws.com/')[1]
                s3_client.delete_object(Bucket=bucket_name, Key=old_file_key)

            # Subir el archivo a S3
            s3_client.upload_fileobj(image_file, bucket_name, file_key)
            
            # Obtener la URL de la imagen
            image_url = f'https://{bucket_name}.s3.amazonaws.com/{file_key}'
            
            # Guardar la URL en el modelo Venture
            
            category.image = image_url
            category.save()
            
            return Response(self.responseRequest(True, 'Actualizado correctamente.', {'image_url': image_url}, 200), status=status.HTTP_200_OK)
        
        except Category.DoesNotExist:
            return Response(self.responseRequest(False, 'No se encontró ninguna instancia de Categoria para este usuario.', {}, 404), status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response(self.responseRequest(False, f'Error al subir la imagen: {str(e)}', {}, 500), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    def addProduct(self, request):
        pass

    def addPromotion(self, request):
        pass

    def getCategories(self, request):
        try:
            user_id = request.user.id
            category = Category.objects.filter(user_id=user_id)
            serializer = CategorySerializer(category, many=True)
            return Response(self.responseRequest(True, f'Success', serializer.data, 200), status=200)
        except Category.DoesNotExist:
            return Response(self.responseRequest(False, f'No se pudo encontrar categorias.', {}, 404), status=status.HTTP_404_NOT_FOUND)


    def deleteCategory(self, request, id):
        user_id = request.user.id
        try:
            category = Category.objects.get(user_id=user_id, id=id)
            
            s3_client = self.getS3Client()
            
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            name = category.name
            name =  name.lower().replace(" ", "-") + f"-{category.id}"
            file_key = f'images/categories/{request.user.id}/{name}'  # Nombre del archivo en S3
            
            # Eliminar la imagen anterior si existe
            if category.image != "":
                # Extraer la clave del archivo anterior desde la URL almacenada
                old_file_key = category.image.split(f'https://{bucket_name}.s3.amazonaws.com/')[1]
                s3_client.delete_object(Bucket=bucket_name, Key=old_file_key)

            category.delete()

            return Response(self.responseRequest(True, 'Categoria eliminada correctamente.', {}, 200), status=status.HTTP_200_OK)
        
        except Category.DoesNotExist:
            return Response(self.responseRequest(False, 'No se pudo encontrar la categoria.', {}, 404), status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(self.responseRequest(False, f'Error: {str(e)}', {}, 500), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
