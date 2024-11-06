from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from users.models import CustomUser

class RegisterAccountSerializer(serializers.ModelSerializer):
  """
  Serializer for registering a new user account.
  Handles creating a new user with hashed password.
  """

  class Meta:
    model = CustomUser
    fields = ["name", "email", "password"]
    extra_kwargs = {
        'password': {'write_only': True}  # Ensures password is write-only
    }

  def create(self, validated_data):
    """
    Create a new user with a hashed password.

    Args:
        validated_data (dict): Validated data containing 'email', 'name', and 'password'.

    Returns:
        CustomUser: The created user instance.

    Raises:
        serializers.ValidationError: If user creation fails.
    """
    try:
      # Create the user without setting the password directly
      user = CustomUser.objects.create(
        email=validated_data['email'],
        name=validated_data['name']
      )

      # Set the password with hashing
      user.set_password(validated_data['password'])
      user.save()
      return user
    except Exception as e:
      raise serializers.ValidationError(f"Error creating user: {str(e)}")


class ChangePasswordSerializer(serializers.Serializer):
  """
  Serializer for handling password change requests.
  Validates old password, ensures new password confirmation,
  and updates the user’s password.
  """
  old_password = serializers.CharField(write_only=True, required=True)
  new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
  new_password2 = serializers.CharField(write_only=True, required=True)

  class Meta:
    model = CustomUser
    fields = ["old_password", "new_password", "new_password2"]

    def validate(self, attrs):
      """
      Validate if the new passwords match.

      Args:
          attrs (dict): Contains 'new_password' and 'new_password2' for confirmation.

      Returns:
          dict: Validated attributes.

      Raises:
          serializers.ValidationError: If new passwords do not match.
      """
      if attrs['new_password'] != attrs['new_password2']:
        raise serializers.ValidationError({"new_password": "The two password fields didn't match."})
      return attrs

    def validate_old_password(self, value):
      """
      Validate if the provided old password matches the user's current password.

      Args:
          value (str): The old password to check.

      Returns:
          str: The validated old password.

      Raises:
          serializers.ValidationError: If the old password is incorrect.
      """
      # Retrieve the user from the request context safely
      user = self.context.get('request').user if self.context.get('request') else None
      if not user or not user.check_password(value):
        raise serializers.ValidationError({"old_password": "Old password is not correct"})
      return value

    def update(self, instance, validated_data):
      """
      Update the user's password after validation.

      Args:
          instance (CustomUser): The user instance whose password is being updated.
          validated_data (dict): Validated data containing the new password.

      Returns:
          CustomUser: The updated user instance.

      Raises:
          serializers.ValidationError: If saving the new password fails.
      """
      try:
        # Set and save the new password securely
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance
      except Exception as e:
        raise serializers.ValidationError(f"Error updating password: {str(e)}")

