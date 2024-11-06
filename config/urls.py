from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
  # user apis (register, login, refresh-token)
  path('api/v1/', include('users.urls')),

  # tasks api
  path('api/v1/', include("tasks.urls")),
]