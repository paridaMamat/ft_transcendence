from django.urls import path, include
from django.contrib.auth.models import User
from .models.CustomUser import *
from .models.Game import *
from .models.Party import *
from .models.UserStats import *
from .models.Lobby import *
from .models.Tournament import *
from rest_framework import serializers

# serializer is used to transform the models data into json data we can work with
# serializer for the welcome page

#################################################
#                                               #
#             CustomUser Serializers            #
#                                               #
#################################################

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','avatar','level','status']

# serializer for the settings
class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username','avatar','email','first_name', 'last_name']

# serializer for global infos
class FullUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','level','status', 'friends','email',
                  'first_name', 'last_name', 'avatar','level',
                  'status','date_joined', 'stat']
        
#################################################
#                                               #
#             UserStats Serializers             #
#                                               #
#################################################
     
class UserStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStatsByGame
        fields = ['user', 'level', 'time', 'nb_parties', 'won_parties', 
                  'parties_ratio', 'highest_score', 'lowest_score', 
                  'played_tour', 'won_tour']

#################################################
#                                               #
#             Game Serializers                  #
#                                               #
#################################################

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id','name', 'img', 'description', 'rules', 
                  'points_to_win', 'stats', 'lobby', 'tournament']

class GameStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameStats
        fields = ['id','game', 'parties_played','played_time', 'avg_game_time']


#################################################
#                                               #
#             Party Serializers                 #
#                                               #
#################################################

class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = ['id', 'game', 'player1', 'player2', 'score1', 'score2', 
                  'duration', 'winner']

class PartyInTournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartyInTournament
        fields = ['id', 'party', 'tournament', 'round_nb', 'index']

#################################################
#                                               #
#             Lobby Serializers                 #
#                                               #
#################################################

class LobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Lobby
        fields = ['id', 'game', 'users']

class UserInLobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInLobby
        fields = ['id', 'user', 'lobby', 'entry_at']

#################################################
#                                               #
#             Tournaments Serializers           #
#                                               #
#################################################

class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ['id', 'tour_name', 'tour_game', 'tour_creator',
                  'creation_date','nb_rounds', 'parties','nb_players', 
                  'duration', 'tour_users', 'winner', 'status']
