from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics
from rest_framework.response import Response

from users.models import CustomUser
from .serializer import RegisterAccountSerializer, ChangePasswordSerializer

class RegisterAccountView(APIView):
  def post(self, request):
    email = request.data.get('email')
    # existing user with same email check
    if CustomUser.objects.filter(email=email).exists():
      return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = RegisterAccountSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


class ChangePasswordView(generics.UpdateAPIView):
  serializer_class = (IsAuthenticated)
  model = CustomUser
  serializer_class = ChangePasswordSerializer

  def __get_user(self, request):
    user = CustomUser.objects.get(email=request.data['email'])
    if not user.exists():
      return Response({"error": "User Does not exists"}, status=status.HTTP_400_BAD_REQUEST)
    return user

  def update(self, request):
    user = self.__get_user()
    serializer = RegisterAccountSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)
