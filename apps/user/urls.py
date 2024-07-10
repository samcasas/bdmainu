from django.urls import re_path
from .views import UserView

urlpatterns = [
    re_path('register', UserView.as_view(), name='register'),
    re_path('login/', UserView.as_view(), name='login'),
    re_path('update/', UserView.as_view(), name='update'),
]