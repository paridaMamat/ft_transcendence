from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from ..models import *
from ..serializers import *
from rest_framework import viewsets, status, permissions
from rest_framework.permissions import BasePermission
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
import json
# from django.utils import timezone
import math
import logging

logger = logging.getLogger(__name__)

class PartyViewSet(viewsets.ModelViewSet):
    queryset = Party.objects.all()
    serializer_class = PartySerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request): #POST method
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # Saves the new object
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):  # allow the current party to get his infos via url localhost/api/users/me
        party = request.party
        serializer = self.get_serializer(party)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None): # GET method
        queryset = self.get_queryset()
        party = get_object_or_404(queryset, pk=pk)  # Fetches by primary key
        serializer = self.get_serializer(party)
        return Response(serializer.data)

    def update(self, request, pk=None): # PUT method
        queryset = self.get_queryset()
        party = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(party, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # Updates the existing object
        
        game = request.data.get('game')
        user1 = request.data.get('player1')
        user2 = request.data.get('player2')
        score1 = request.data.get('score1')
        score2 = request.data.get('score2')
        duration = request.data.get('end_time') - request.data.get('start_time')
        winner = request.data.get('winner_name')
        
        #qui a gagner
        if user1.username == winner:
            win1 = True
            win2 = False
        else:
            win1 = False
            win2 = True
        # une partie dans un tournoi ?
        if request.data.get('type') is 'Matchmaking':
            tour = False
            tour_win1 = False
            tour_win2 = False        
        else:
            tour = True
            #filtre supp a ajouter pour mise a jour du winner du tournoi.
            tour_win1 = False
            tour_win2 = False

        try:
            userStat1 = UserStatsByGame.objects.filter(game=game, user=user1)
            userStat1.updateUserData(duration, win1, tour, tour_win1, score1)
        except UserStatsByGame.DoesNotExist:
            return Response({"detail": "Player1 not found."}, status=404)
        
        try:
            userStat2 = UserStatsByGame.objects.filter(game=game, user=user2)
            userStat2.updateUserData(duration, win2, tour, tour_win2, score2)
        except UserStatsByGame.DoesNotExist:
            return Response({"detail": "Player2 not found."}, status=404)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def retrievePartyByGame(self, request, game_id=None, user_id=None):
        if not game_id or not user_id:
            return Response({"detail": "Both game_id and user_id URL parameters are required."}, status=400)

        try:
            game = Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            return Response({"detail": "Game not found."}, status=404)
        
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"detail": "Player not found."}, status=404)

        queryset = self.get_queryset().filter(game=game, player1=user, tour='Matchmaking').order_by('date')[:5]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    