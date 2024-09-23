from django.urls import path
from .views import SubscriptionsView, SubscriptionsCRMView

urlpatterns = [
    
    #POST
    path('add-plan', SubscriptionsCRMView.as_view(action='add_plan'), name='add-plan'),
    path('add-promotional-code', SubscriptionsCRMView.as_view(action='add_promotional_code'), name='add-promotional-code'),
    path('use-promotional-code', SubscriptionsView.as_view(action='use_promotional_code'), name='use-promotional-code'),
    #GET
    
    
    #DELETE
    
]
