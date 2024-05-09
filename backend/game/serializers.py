from django.urls import path, include
from django.contrib.auth.models import User
from .models import Game, Party, PartyStats, Lobby, UserInLobby, Tournament
from website.models import CustomUser
from rest_framework import serializers

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id','game_name', 'img', 'description', 'rules', 'points_to_win', 'nb_parties_played']

class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = ['id', 'players', 'duration','date', 'winner']

class PartyStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartyStats
        fields = ['id', 'user_id', 'won_set', 'lost_set', 'ratio', 'score', 'winner']

class LobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Lobby
        fields = ['id', 'game', 'users']

class UserInLobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInLobby
        fields = ['id', 'user', 'lobby', 'entry_at']

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