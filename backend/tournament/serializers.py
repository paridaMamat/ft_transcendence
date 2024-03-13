from rest_framework import serializers
from .models import Tournament, TournamentMatch, Player

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'name')

class TournamentMatchSerializer(serializers.ModelSerializer):
    player1 = PlayerSerializer(read_only=True)
    player2 = PlayerSerializer(read_only=True)
    winner = PlayerSerializer(read_only=True)

    class Meta:
        model = TournamentMatch
        fields = ('id', 'player1', 'player2', 'winner', 'round', 'match_id')

class TournamentSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, read_only=True)
    matchs = TournamentMatchSerializer(many=True, read_only=True)
    
    class Meta:
        model = Tournament
        fields = ('id', 'name', 'players', 'matchs', 'online', 'rounds', 'current_round', 'finished')
