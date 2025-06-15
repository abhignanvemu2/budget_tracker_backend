from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from helpers import USER_ERRORS

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True, min_length = 8)
    password_confirm = serializers.CharField(write_only = True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError(USER_ERRORS.PASSWORD_DONT_MATCH)
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username = username, password = password)
            if not user:
                raise serializers.ValidationError(USER_ERRORS.INVALID_CREDENTIALS)
            if not user.is_active:
                raise serializers.ValidationError(USER_ERRORS.USER_ACCOUNT_IS_DISABLED)
            attrs['user'] = user
        else:
            raise serializers.ValidationError(USER_ERRORS.MUST_INCLUDE_USERNAME_PASSWORD)
        return attrs

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined')