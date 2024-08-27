from django.urls import re_path, path
from .views import VentureView


urlpatterns = [
    re_path('set-venture', VentureView.as_view(), name='set-venture'),
    re_path('new-branch', VentureView.as_view(), name='new-branch'),
    re_path('put-branch', VentureView.as_view(), name='put-branch'),
    re_path('get-branch/(?P<id>\d+)$', VentureView.as_view(), name='get-branch'),
    re_path('get-venture-information', VentureView.as_view(), name='get-venture-information'),
]