from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
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
        #categories
        if self.action == 'add_category':
            return self.addCategory(request)
        elif self.action == 'update_category':
            return self.updateCategory(request)
        elif self.action == 'upload_image_category':
            return self.uploadImageCategory(request)
        
        #products
        elif self.action == 'add_product':
            return self.addProduct(request)
        elif self.action == 'update_product':
            return self.updateProduct(request)
        elif self.action == 'upload_image_product':
            return self.uploadImageProduct(request)
        
        #promotions
        elif self.action == 'add_promotion':
            return self.addPromotion(request)
        elif self.action == 'update_promotion':
            return self.updatePromotion(request)
        elif self.action == 'upload_image_promotion':
            return self.uploadImagePromotion(request)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id=None, *args, **kwargs):
        if self.action == 'get_categories':
            return self.getCategories(request)
        elif self.action == 'get_promotions':
            return self.getPromotions(request)
        elif self.action == 'get_products':
            return self.getProducts(request)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id=None, *args, **kwargs):
        if self.action == 'delete_category' and id is not None:
            return self.deleteCategory(request, id)
        elif self.action == 'delete_promotion' and id is not None:
            return self.deletePromotion(request, id)
        elif self.action == 'delete_product' and id is not None:
            return self.deleteProduct(request, id)
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
        

    def addPromotion(self, request):
        promotion_data = JSONParser().parse(request)
        user_id = request.user.id
        try:
            promotion_data['user_id'] = user_id
            promotion_data['status'] = 1 if promotion_data['status'] == True else 0
            serializer = PromotionSerializer(data=promotion_data)
            if serializer.is_valid():
                serializer.save()
                return Response(self.responseRequest(True, 'Promoción creada correctamente.', serializer.data, 201), status=status.HTTP_201_CREATED)
            
            return Response(self.responseRequest(False, 'No se pudo crear la promoción.', {}, 409), status=status.HTTP_409_CONFLICT)
        
        except Exception as e:
            return Response(self.responseRequest(False, f'No se pudo crear la promoción. Error: {str(e)}', {}, 500), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def updatePromotion(self, request):
        promotion_data = JSONParser().parse(request)
        user_id = request.user.id
        try:
            promotion = Promotion.objects.get(id=promotion_data['id'])
            promotion_data['user_id'] = user_id
            promotion_data['status'] = 1 if promotion_data['status'] == True else 0
            serializer = PromotionSerializer(promotion, data=promotion_data)
            if serializer.is_valid():
                serializer.save()
                return Response(self.responseRequest(True, 'Promoción actualizada correctamente.', serializer.data, 200), status=status.HTTP_200_OK)
            
            return Response(self.responseRequest(False, 'No se pudo actualizar la promoción.', serializer.errors, 409), status=status.HTTP_409_CONFLICT)
        
        except Promotion.DoesNotExist:
            return Response(self.responseRequest(False, 'Promoción no encontrada.', {}, 404), status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response(self.responseRequest(False, f'No se pudo actualizar la promoción. Error: {str(e)}', {}, 500), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def uploadImagePromotion(self, request):
        # Obtener el archivo de imagen
        image_file = request.FILES.get('image')
        promotion_id = request.data.get('promotion_id')
        if not image_file:
            return Response(self.responseRequest(False, 'No se encontró ninguna imagen en la solicitud.', {}, 400), status=status.HTTP_400_BAD_REQUEST)
        
        try:
            promotion = Promotion.objects.get(id=promotion_id)
            # Subir la imagen a S3
            s3_client = self.getS3Client()
            
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            name = promotion.name
            name = name.lower().replace(" ", "-") + f"-{promotion.id}"
            file_key = f'images/promotions/{request.user.id}/{name}'  # Nombre del archivo en S3
            
            # Eliminar la imagen anterior si existe
            if promotion.image != "":
                old_file_key = promotion.image.split(f'https://{bucket_name}.s3.amazonaws.com/')[1]
                s3_client.delete_object(Bucket=bucket_name, Key=old_file_key)

            # Subir el archivo a S3
            s3_client.upload_fileobj(image_file, bucket_name, file_key)
            
            # Obtener la URL de la imagen
            image_url = f'https://{bucket_name}.s3.amazonaws.com/{file_key}'
            
            # Guardar la URL en el modelo
            promotion.image = image_url
            promotion.save()
            
            return Response(self.responseRequest(True, 'Imagen de promoción actualizada correctamente.', {'image_url': image_url}, 200), status=status.HTTP_200_OK)
        
        except Promotion.DoesNotExist:
            return Response(self.responseRequest(False, 'No se encontró ninguna instancia de Promoción.', {}, 404), status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response(self.responseRequest(False, f'Error al subir la imagen: {str(e)}', {}, 500), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def getPromotions(self, request):
        try:
            user_id = request.user.id
            promotions = Promotion.objects.filter(user_id=user_id)
            serializer = PromotionSerializer(promotions, many=True)
            return Response(self.responseRequest(True, 'Promociones obtenidas correctamente.', serializer.data, 200), status=status.HTTP_200_OK)
        except Promotion.DoesNotExist:
            return Response(self.responseRequest(False, 'No se encontraron promociones.', {}, 404), status=status.HTTP_404_NOT_FOUND)

    def deletePromotion(self, request, id):
        user_id = request.user.id
        try:
            promotion = Promotion.objects.get(user_id=user_id, id=id)
            
            s3_client = self.getS3Client()
            
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            name = promotion.name
            name = name.lower().replace(" ", "-") + f"-{promotion.id}"
            file_key = f'images/promotions/{request.user.id}/{name}'  # Nombre del archivo en S3
            
            # Eliminar la imagen anterior si existe
            if promotion.image != "":
                old_file_key = promotion.image.split(f'https://{bucket_name}.s3.amazonaws.com/')[1]
                s3_client.delete_object(Bucket=bucket_name, Key=old_file_key)

            promotion.delete()

            return Response(self.responseRequest(True, 'Promoción eliminada correctamente.', {}, 200), status=status.HTTP_200_OK)
        
        except Promotion.DoesNotExist:
            return Response(self.responseRequest(False, 'No se pudo encontrar la promoción.', {}, 404), status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response(self.responseRequest(False, f'Error al eliminar la promoción: {str(e)}', {}, 500), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def addProduct(self, request):
        product_data = JSONParser().parse(request)
        user_id = request.user.id
        try:
            product_data['user_id'] = user_id
            product_data['status'] = 1 if product_data['status'] == True else 0
            serializer = ProductSerializer(data=product_data)
            if serializer.is_valid():
                serializer.save()
                return Response(self.responseRequest(True, 'Producto creado correctamente.', serializer.data, 201), status=status.HTTP_201_CREATED)
            
            return Response(self.responseRequest(False, 'No se pudo crear el producto.', {}, 409), status=status.HTTP_409_CONFLICT)
        
        except Exception as e:
            return Response(self.responseRequest(False, f'No se pudo crear el producto. Error: {str(e)}', {}, 500), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def updateProduct(self, request):
        product_data = JSONParser().parse(request)
        user_id = request.user.id
        try:
            product = Product.objects.get(id=product_data['id'])
            product_data['user_id'] = user_id
            product_data['status'] = 1 if product_data['status'] == True else 0
            serializer = ProductSerializer(product, data=product_data)
            if serializer.is_valid():
                serializer.save()
                return Response(self.responseRequest(True, 'Producto actualizado correctamente.', serializer.data, 200), status=status.HTTP_200_OK)
            
            return Response(self.responseRequest(False, 'No se pudo actualizar el producto.', serializer.errors, 409), status=status.HTTP_409_CONFLICT)
        
        except Product.DoesNotExist:
            return Response(self.responseRequest(False, 'Producto no encontrado.', {}, 404), status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response(self.responseRequest(False, f'No se pudo actualizar el producto. Error: {str(e)}', {}, 500), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def uploadImageProduct(self, request):
        image_file = request.FILES.get('image')
        product_id = request.data.get('product_id')

        if not image_file:
            return Response(self.responseRequest(False, 'No se encontró ninguna imagen en la solicitud.', {}, 400), status=status.HTTP_400_BAD_REQUEST)
        
        try:
            product = Product.objects.get(id=product_id)
            # Subir la imagen a S3
            s3_client = self.getS3Client()
            
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            name = product.name
            name = name.lower().replace(" ", "-") + f"-{product.id}"
            file_key = f'images/products/{request.user.id}/{name}'
            
            # Eliminar la imagen anterior si existe
            if product.image:
                old_file_key = product.image.split(f'https://{bucket_name}.s3.amazonaws.com/')[1]
                s3_client.delete_object(Bucket=bucket_name, Key=old_file_key)

            # Subir el archivo a S3
            s3_client.upload_fileobj(image_file, bucket_name, file_key)
            
            # Obtener la URL de la imagen
            image_url = f'https://{bucket_name}.s3.amazonaws.com/{file_key}'
            
            # Guardar la URL en el modelo
            Product.objects.filter(id=product_id).update(image=image_url)
            
            return Response(self.responseRequest(True, 'Imagen del producto actualizada correctamente.', {'image_url': image_url}, 200), status=status.HTTP_200_OK)
        
        except Product.DoesNotExist:
            return Response(self.responseRequest(False, 'No se encontró ninguna instancia de Producto.', {}, 404), status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response(self.responseRequest(False, f'Error al subir la imagen: {str(e)}', {}, 500), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def deleteProduct(self, request, id):
        user_id = request.user.id
        try:
            product = Product.objects.get(user_id=user_id, id=id)
            
            s3_client = self.getS3Client()
            
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            name = product.name
            name = name.lower().replace(" ", "-") + f"-{product.id}"
            file_key = f'images/products/{request.user.id}/{name}'  # Nombre del archivo en S3
            
            # Eliminar la imagen anterior si existe
            if product.image != "":
                old_file_key = product.image.split(f'https://{bucket_name}.s3.amazonaws.com/')[1]
                s3_client.delete_object(Bucket=bucket_name, Key=old_file_key)

            product.delete()

            return Response(self.responseRequest(True, 'Producto eliminado correctamente.', {}, 200), status=status.HTTP_200_OK)
        
        except Product.DoesNotExist:
            return Response(self.responseRequest(False, 'No se pudo encontrar el producto.', {}, 404), status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(self.responseRequest(False, f'Error: {str(e)}', {}, 500), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def getProducts(self, request):
        try:
            user_id = request.user.id
            products = Product.objects.filter(user_id=user_id)
            serializer = ProductSerializer(products, many=True)
            return Response(self.responseRequest(True, 'Productos obtenidos con éxito.', serializer.data, 200), status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response(self.responseRequest(False, 'No se encontraron productos.', {}, 404), status=status.HTTP_404_NOT_FOUND)