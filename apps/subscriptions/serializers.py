from rest_framework import serializers
from apps.subscriptions.models.Plan import Plan
from apps.subscriptions.models.PaymentMethod  import PaymentMethod 
from apps.subscriptions.models.Subscription import Subscription
from apps.subscriptions.models.PromotionalCode import PromotionalCode
from apps.subscriptions.models.Benefit import Benefit


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

class PromotionalCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionalCode
        fields = '__all__'

class BenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Benefit
        fields = '__all__'