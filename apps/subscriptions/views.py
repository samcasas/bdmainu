from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.resources.helpers import Helper
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# MODELS / SERIALIZERS
from apps.subscriptions.models.Plan import Plan
from apps.subscriptions.models.Benefit import Benefit
from apps.subscriptions.models.PaymentMethod  import PaymentMethod 
from apps.subscriptions.models.Subscription import Subscription
from apps.subscriptions.models.PromotionalCode import PromotionalCode
from apps.user.models import User
from .serializers import PlanSerializer, PaymentMethodSerializer, SubscriptionSerializer, PromotionalCodeSerializer


class SubscriptionsCRMView(APIView, Helper):
    action = None
    #permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.action = kwargs.get('action')

    def post(self, request, *args, **kwargs):
        
        if self.action == 'add_plan':
            return self.add_plan(request)
        elif self.action == 'add_promotional_code':
            return self.add_promotional_code(request)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    
    def add_plan(self, request):
        try:
            serializer = PlanSerializer(data=request.data)
            
            if serializer.is_valid():
                # Intentar guardar el plan y ver si es donde ocurre el error
                serializer.save()
                return Response(self.responseRequest(False, 'Plan creado correctamente', {}, 200), status=status.HTTP_201_CREATED)
            else:
                return Response(self.responseRequest(True, 'No se pudo crear el plan, revisa los datos.', {}, 400), status=status.HTTP_400_BAD_REQUEST)
        
        except AttributeError as e:
            # Atrapa el error específico de atributo y muestra más detalles
            return Response(self.responseRequest(True, f'Error de atributo: {str(e)}', {}, 500), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        except Exception as e:
            # Manejo genérico de excepciones
            return Response(self.responseRequest(True, f'Ocurrió un error inesperado: {str(e)}', {}, 500), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def add_promotional_code(self, request):

        serializer = PromotionalCodeSerializer(data=request.data)
        print(serializer.is_valid())
        # Validación de datos
        if serializer.is_valid():
            serializer.save()  # Guarda el nuevo plan
            return Response(self.responseRequest(False, f'Codigo creado correctamente', {}, 200), status=status.HTTP_201_CREATED)
        else:
            return Response(self.responseRequest(False, f'No se pudo crear el codigo, revisa los datos.', {}, 400), status=status.HTTP_400_BAD_REQUEST)
    

class SubscriptionsView(APIView, Helper):
    action = None
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.action = kwargs.get('action')

    def post(self, request, *args, **kwargs):
        if self.action == 'use_promotional_code':
            return self.subscribe_by_promotional_code(request)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def subscribe_by_promotional_code(self, request):
        data = JSONParser().parse(request)
        try:
            user = User.objects.get(id=request.user.id)
            if user.subscription_id is not None:
                return Response(self.responseRequest(False, 'Ya cuentas con una suscripción activa.', {}, 400), status=status.HTTP_400_BAD_REQUEST)

            validation = Subscription.code_validation(data['code'], data['plan_id'])
            if not validation["isValid"]:
                return Response(self.responseRequest(False, validation["message"], {}, 400), status=status.HTTP_400_BAD_REQUEST)

            
            
            codeObj =  PromotionalCode.getObjectCode(data['code'])
            # Calcular la fecha de expiración
            current_date = datetime.now().date()
            expiration_date = current_date + relativedelta(months=codeObj.months)  # Sumar los meses

            # Crear y guardar la nueva suscripción
            subscription_data = {
                'user_id': request.user.id,
                'plan_id': data['plan_id'], # Puedes manejar esto como opcional
                'code_id': codeObj.id,
                'expiration_date': expiration_date
            }

            serializer = SubscriptionSerializer(data=subscription_data)
            # Descontar el código promocional
            if serializer.is_valid():
                subscription = serializer.save() # Guarda la nueva suscripción
                user.subscription_id = subscription.id
                user.save()
                
                PromotionalCode.discountCode(data['code'])
                
                return Response(self.responseRequest(True, 'Suscripción realizada correctamente.', {}, 201), status=status.HTTP_201_CREATED)
            else:
                return Response(self.responseRequest(False, 'Error al suscribirse.', {}, 400), status=status.HTTP_400_BAD_REQUEST)
            
        except User.DoesNotExist:
            return Response(self.responseRequest(True, 'Usuario no encontrado.', {}, 404), status=status.HTTP_404_NOT_FOUND)
 
        except Exception as e:
            return Response(self.responseRequest(True, f'Ocurrió un error inesperado: {str(e)}', {}, 500), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

