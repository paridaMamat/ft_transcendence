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
        fields = ['username','avatar','level','status',
                  'friends','email','first_name', 'last_name',
                  'avatar','level','status','date_joined']
        
#################################################
#                                               #
#             UserStats Serializers             #
#                                               #
#################################################
     
class UserStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStatsByGame
        fields = ['user', 'rank', 'time', 'nb_parties', 'won_parties', 
                  'parties_ratio', 'highest_score', 'lowest_score', 'played_tour', 'won_tour']

#################################################
#                                               #
#             Game Serializers                  #
#                                               #
#################################################

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id','game_name', 'img', 'description', 'rules', 'points_to_win', 'nb_parties_played']

#################################################
#                                               #
#             Party Serializers                 #
#                                               #
#################################################

class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = ['id', 'players', 'duration','date', 'winner']

class PartyInTournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartyInTournament
        fields = ['id', 'party', 'round_nb', 'index']

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
        fields = ['tour_id', 'tour_name', 'tour_game', 'tour_creator',
                  'creation_date','nb_rounds', 'nb_players', 
                  'start_time', 'tour_users', 'winner']

class TournamentRoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ['tour_name', 'tour_game', 'tour_creator', 'current_round'
                  'creation_date','nb_rounds', 'current_round', 'nb_players', 
                  'duration', 'tour_users', 'round_winner']

class TournamentEndSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ['tour_name', 'tour_game', 'tour_creator', 'nb_rounds', 'nb_players', 
                  'duration', 'tour_users', 'winner']