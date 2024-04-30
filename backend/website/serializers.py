from django.urls import path, include
from django.contrib.auth.models import User
from .models import CustomUser

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','avatar','level','status']

class FullUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','avatar','level','status',
                  'friends','email','first_name', 'last_name',
                  'avatar','level','status','date_joined']