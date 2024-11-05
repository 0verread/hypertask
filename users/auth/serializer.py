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
    """
    # Create user without setting the password directly
    user = CustomUser.objects.create(
        email=validated_data['email'],
        name=validated_data['name']
    )
      
    # Set the password with hashing
    user.set_password(validated_data['password'])
    user.save()
    return user

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
    fields = ["old_password", "password", "password"]

  def validate(self, attrs):
    """
    Check if the new passwords match.
    """
    # Confirm that the two new password fields match
    if attrs['new_password'] != attrs['new_password2']:
        raise serializers.ValidationError({"new_password": "The two password fields didn't match."})
    return attrs

  def validate_old_password(self, value):
    """
    Check if the provided old password is correct.
    """
    user = self.context['request'].user
    if not user.check_password(value):
      raise serializers.ValidationError({"old_password": "Old password is not correct"})
    return value

  def update(self, instance, validated_data):
    """
    Update the user password after validation.
    """
    instance.set_password(validated_data['new_password'])
    instance.save()
    return instance
