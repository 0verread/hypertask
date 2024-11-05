from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework import status
from django.contrib.auth import authenticate

from .auth.serializer import RegisterAccountSerializer
from .models import CustomUser

class CustomTokenObtainPairView(TokenObtainPairView):
	def post(self, request, *args, **kwargs):
		email = request.data.get("email")
		password = request.data.get("password")

		# Check if the email exists and validate credentials
		try:
				user = CustomUser.objects.get(email=email)
		except CustomUser.DoesNotExist:
				return Response({"message": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

		# Attempt to authenticate the user with the provided email and password
		user = authenticate(request, email=email, password=password)
		if user is None:
				return Response({"message": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

		# If authentication is successful, proceed with the default token generation
		return super().post(request, *args, **kwargs)
	
class AccountView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get(self, request):
      serializer = RegisterAccountSerializer(request.user, many=False)
      return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutView(APIView):
	permission_classes = (IsAuthenticated,)
	parser_classes = [JSONParser, MultiPartParser, FormParser]

	def post(self, request):
		try:
			refresh_token = request.data["refresh_token"]
			print(refresh_token)
			token = RefreshToken(refresh_token)
			# Refresh Token doesn't get destroyed, blacklist it
			token.blacklist()
			return Response({"message": f"logout success"}, status=status.HTTP_205_RESET_CONTENT)
		except Exception as e:
			return Response({"message": f"logout failed, error: {e}"}, status=status.HTTP_400_BAD_REQUEST)

