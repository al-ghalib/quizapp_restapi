from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(
        write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, attrs):
        # Checking two password match
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "The two password fields must match."})
        return attrs

    def create(self, validated_data):
        # Creating a new user with the validated data
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user
