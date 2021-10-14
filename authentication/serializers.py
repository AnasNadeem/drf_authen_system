from authentication.models import User
from rest_framework import serializers
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        if not username.isalnum():
            raise serializers.ValidationError('Username should contain alphanumeric characters only')

        return attrs

    def create(self, validated_data):
        return User.object.create_user(**validated_data)

class EmailVerificationSerializer(serializers.ModelSerializer):
  token = serializers.CharField(max_length=55)

  class Meta:
    model = User
    fields = ['token']