from django.urls import re_path
from apps.user.views import AuthView, UserView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    re_path('register', AuthView.as_view(), name='register'),
    re_path('login', AuthView.as_view(), name='login'),
    re_path('confirmation', AuthView.as_view(), name='confirmation'),
    re_path('resend-verify', AuthView.as_view(), name='resend-verify'),

    re_path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    re_path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    re_path('put-profile', UserView.as_view(action='update_user'), name='put-profile'),
    re_path('profile-image', UserView.as_view(action='upload_image_profile'), name='profile-image'),
    re_path('get-profile', UserView.as_view(action='get_profile_data'), name='get-profile'),

]