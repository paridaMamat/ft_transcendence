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
    class Meta:
        model = CustomUser
        fields =('__all__')
        # ['id','username','first_name', 'last_name', 'level','status',
        #          'email', 'avatar','level','status','date_joined','friends', 
        #          'two_factor_enabled', 'two_factor_secret']
        extra_kwargs = {
            'password': {'write_only': True},
            'two_factor_secret': {'write_only': True},  # You may choose to keep this field write-only
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
        
#################################################
#                                               #
#             UserStats Serializers             #
#                                               #
#################################################
     
class UserStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStatsByGame
        fields = ('__all__')
        #['id', 'game', 'user', 'level', 'time_played', 'played_parties', 
        #          'won_parties', 'parties_ratio', 'highest_score', 
        #          'lowest_score', 'played_tour', 'won_tour', 'tour_ratio']

#################################################
#                                               #
#             Game Serializers                  #
#                                               #
#################################################

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('__all__')
        #['id','name', 'img', 'description', 'rules', 
                #  'points_to_win', 'stats', 'lobby', 'tournament']

class GameStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameStats
        fields = ('__all__')
        #['id','game', 'parties_played','played_time', 'avg_game_time']

#################################################
#                                               #
#             Party Serializers                 #
#                                               #
#################################################

class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = ('__all__')
        #['id', 'game', 'player1', 'player2', 'score1', 'score2', 
                #  'duration', 'winner']

class PartyInTournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartyInTournament
        fields = ('__all__')
        #['id', 'party', 'tournament', 'round_nb', 'index']

#################################################
#                                               #
#             Lobby Serializers                 #
#                                               #
#################################################

class LobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Lobby
        fields = ('__all__')
        #['id', 'game', 'users']

class UserInLobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInLobby
        fields = ('__all__')
        #['id', 'user', 'lobby', 'entry_at']

#################################################
#                                               #
#             Tournaments Serializers           #
#                                               #
#################################################

class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ('__all__')
        #['id', 'tour_name', 'tour_game', 'tour_creator',
        #          'creation_date','nb_rounds', 'parties','nb_players', 
        #          'duration', 'tour_users', 'winner', 'status']
