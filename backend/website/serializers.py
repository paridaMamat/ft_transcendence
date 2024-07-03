from .models.CustomUser import *
from .models.Game import *
from .models.Party import *
from .models.UserStats import *
from .models.Lobby import *
from .models.Tournament import *
from rest_framework import serializers
from django.contrib.auth import authenticate

# serializer is used to transform the models data into json data we can work with

#################################################
#                                               #
#             CustomUser Serializers            #
#                                               #
#################################################

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)
            if not user:
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

class CustomUserSerializer(serializers.ModelSerializer):
    friends = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), many=True)
    
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'two_factor_secret': {'write_only': True},  # Keep this field write-only if necessary
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
    
#################################################
#                                               #
#             UserStats Serializers             #
#                                               #
#################################################
     
class UserStatsSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    avatar = serializers.CharField(source='user.avatar', read_only=True)

    class Meta:
        model = UserStatsByGame
        fields = ['id', 'game', 'username', 'avatar', 'time_played', 'level', 'score', 'played_parties', 
            'won_parties', 'lost_parties', 'parties_ratio', 'played_tour', 'avg_time_per_party',
            'won_tour', 'lost_tour' , 'tour_ratio']
        
#################################################
#                                               #
#             Game Serializers                  #
#                                               #
#################################################

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('__all__')

#################################################
#                                               #
#             Party Serializers                 #
#                                               #
#################################################

class PartySerializer(serializers.ModelSerializer):

    player1 = CustomUserSerializer()
    player2 = CustomUserSerializer()

    class Meta:
        model = Party
        fields = ('__all__')
        
#################################################
#                                               #
#             Lobby Serializers                 #
#                                               #
#################################################

class LobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Lobby
        fields = ('__all__')

class UserInLobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInLobby
        fields = ('__all__')

#################################################
#                                               #
#             Tournaments Serializers           #
#                                               #
#################################################

class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ('__all__')