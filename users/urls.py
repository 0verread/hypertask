from django.urls import path

from rest_framework_simplejwt import views as jwt_views

from .views import CustomTokenObtainPairView, AccountView, LogoutView
from .auth.api import RegisterAccountView, ChangePasswordView
from .views import CustomTokenObtainPairView, AccountView


urlpatterns = [
  # User Auth URLS
  path("users/register", RegisterAccountView.as_view()),
  path("users/login", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
  # get new access token using refresh token,  
  path("users/login/token-refresh", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
  path("users/logout", LogoutView.as_view(), name="auth_logout"),
  path("users/change-pass", ChangePasswordView.as_view(), name="change_password"),
  path("users/me", AccountView.as_view()),
]

