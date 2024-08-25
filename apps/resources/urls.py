from django.urls import re_path
from .views import ResourcesView


urlpatterns = [
    re_path('get-states', ResourcesView.as_view(), name='states'),
    re_path('get-countries', ResourcesView.as_view(), name='countries'),
]