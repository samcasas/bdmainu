from django.urls import re_path
from .views import UserView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    re_path('register', UserView.as_view(), name='register'),
    re_path('login', UserView.as_view(), name='login'),
    re_path('update', UserView.as_view(), name='update'),
    re_path('confirmation', UserView.as_view(), name='confirmation'),
]