from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

app_name = 'accounts'

v1_urlpatterns = [
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/registration/', views.RegistrationAPIView.as_view(), name='registration'),
    path('auth/login/', views.LoginAPIView.as_view(), name='login'),
    path('auth/logout/', views.LogoutAPIView.as_view(), name='logout'),
]
