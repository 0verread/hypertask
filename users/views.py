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
	"""
	Custom view for handling JWT token obtainment.
	Verifies user credentials and provides an access/refresh token pair if valid.
	"""

	def post(self, request, *args, **kwargs):
		"""
		Handle POST request to authenticate user and generate JWT tokens.

		Args:
			request (Request): The incoming HTTP request containing 'email' and 'password'.

		Returns:
			Response: JSON response with JWT token pair or error message.

		Raises:
			serializers.ValidationError: If user credentials are invalid or authentication fails.
		"""
		email = request.data.get("email")
		password = request.data.get("password")

		try:
			# Check if the email exists in the database
			user = CustomUser.objects.get(email=email)
		except CustomUser.DoesNotExist:
			return Response({"message": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

		# Authenticate user using Django's authenticate method
		user = authenticate(request, email=email, password=password)
		if user is None:
			return Response({"message": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

		# If authentication is successful, continue with token generation
		return super().post(request, *args, **kwargs)


class AccountView(APIView):
	"""
	API view to retrieve details of the currently authenticated user.
	"""
	permission_classes = (IsAuthenticated,)
	parser_classes = [JSONParser, MultiPartParser, FormParser]

	def get(self, request):
		"""
		Handle GET request to retrieve user information.

		Args:
			request (Request): The incoming HTTP request from an authenticated user.

		Returns:
			Response: JSON response with user data.
		"""
		serializer = RegisterAccountSerializer(request.user, many=False)
		return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(APIView):
	"""
	API view to log out a user by blacklisting the provided refresh token.
	"""
	permission_classes = (IsAuthenticated,)
	parser_classes = [JSONParser, MultiPartParser, FormParser]

	def post(self, request):
			"""
			Handle POST request to log out the user by blacklisting the refresh token.

			Args:
				request (Request): The incoming HTTP request containing the 'refresh_token'.

			Returns:
				Response: JSON response indicating success or failure of logout.

			Raises:
				serializers.ValidationError: If the refresh token is invalid or missing.
			"""
			try:
				# Retrieve the refresh token from the request data
				refresh_token = request.data.get("refresh_token")
				if not refresh_token:
					return Response({"message": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

				# Attempt to blacklist the refresh token
				token = RefreshToken(refresh_token)
				token.blacklist()  # Blacklists the refresh token

				return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        
			except Exception as e:
				# Handle cases where the token is invalid or any other error occurs
				return Response({"message": f"Logout failed. Error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
