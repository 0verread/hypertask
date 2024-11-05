from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, generics
from rest_framework.permissions import IsAuthenticated

from users.models import CustomUser

class RegisterAccountSerializer(serializers.ModelSerializer):
  class Meta:
    model = CustomUser
    fields = ["name", "email", "password"]
    extra_kwargs = {
        'password': {'write_only': True}
    }

  def create(self, validated_data):
    user = CustomUser.objects.create(email=validated_data['email'],
                                      name=validated_data['name']
                                      )
    user.set_password(validated_data['password'])
    user.save()
    return user

class ChangePasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    new_password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
      model = CustomUser
      fields = ["old_password", "password", "password"]

    def validate(self, attrs):
      if (attrs['password'] != attrs['password2']):
        return serializers.ValidationError({"password": "password fields did not match"})

      return attrs

    def validate_old_password(self, value):
      user = self.context['request'].user 
      if not user.check_password(value):
        return serializers.ValidationError({"old_password": "old password is not correct"})
      return value

    def update(self, validated_data):
      user = CustomUser.objects.get(email=validated_data["email"])
      user.set_password(validated_data['password'])
      user.save()
      return user



