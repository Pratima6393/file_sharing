from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import File

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'user_type')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            user_type=validated_data['user_type'],
            is_active = False if validated_data['user_type'] == 'operation' else True
            
        )
        return user

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('file',)


