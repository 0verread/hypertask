from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework import serializers
from users.models import CustomUser
from .serializer import RegisterAccountSerializer, ChangePasswordSerializer

class RegisterAccountView(APIView):
  """
  API view for registering a new user account.
  """
  def post(self, request):
    """
    Handle POST request to register a new user.
    
    Args:
      request (Request): The incoming HTTP request containing user data (email, password, etc.).

    Returns:
      Response: JSON response with created user data or an error message.

    Raises:
      serializers.ValidationError: If the email is already registered or if validation fails.
    """
    email = request.data.get('email')
    
    # Check if a user with the provided email already exists
    if CustomUser.objects.filter(email=email).exists():
      return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Serialize and validate the incoming data
    serializer = RegisterAccountSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    # Save the new user and respond with the user data
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


class ChangePasswordView(generics.UpdateAPIView):
  """
  API view to allow authenticated users to change their password.
  """
  permission_classes = [IsAuthenticated]
  serializer_class = ChangePasswordSerializer

  def get_object(self):
    """
    Retrieve the current authenticated user.

    Returns:
        CustomUser: The authenticated user instance.
    """
    return self.request.user  # Return the authenticated user instead of a queryset

  def update(self, request, *args, **kwargs):
    """
    Handle the password update request.

    Args:
      request (Request): The incoming HTTP request containing the old and new password.

    Returns:
      Response: JSON response indicating password update status.

    Raises:
      serializers.ValidationError: If password validation or updating fails.
    """
    try:
      user = self.get_object()  # Get the authenticated user
      serializer = self.get_serializer(user, data=request.data, context={'request': request})
      serializer.is_valid(raise_exception=True)  # Validate old password and new passwords
      serializer.save()  # Update the password
      return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
      
    except serializers.ValidationError as ve:
      # Handle validation errors specifically
      return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
      
    except Exception as e:
      # Catch-all for unexpected exceptions
      return Response({"error": "An unexpected error occurred while changing the password."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
