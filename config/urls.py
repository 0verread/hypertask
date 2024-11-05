from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
  path('api/v1/users/', include('users.urls')),
  path('api/v1/users/token', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('api/v1/users/token/refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]