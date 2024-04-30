# views.py
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Game, Party, PartyStats, Lobby, UserInLobby, Tournament
from .serializers import LobbySerializer, UserInLobby, TournamentSerializer
from .serializers import GameSerializer, PartySerializer, PartyStatsSerializer
import requests
