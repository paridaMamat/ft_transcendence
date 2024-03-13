from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    # profile = serializers.ImageField(required=False)
    profile_url = serializers.SerializerMethodField()
    class Meta(object):
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'games_won', 'games_lost', 'language', 'profile_url', 'available')

    def get_profile_url(self, obj):
        if obj.profile:
            return obj.profile.url
        return None
    
    def validate_username(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("The username must contain at least 5 characters.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("The password must contain at least 8 characters.")
        return value