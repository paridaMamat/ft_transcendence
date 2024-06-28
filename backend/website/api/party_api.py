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
from django.utils import timezone
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
        try:
            serializer = self.get_serializer(party, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()  # Updates the existing object
        except Exception as e:
            logger.error("Error: %s", e)
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None): # PUT method
        queryset = self.get_queryset()
        logger.debug("Received request data: %s", request.data)
        party = get_object_or_404(queryset, pk=pk)
        # party.updateEndParty()
        serializer = self.get_serializer(party, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # Updates the existing object
        
        game = party.game
        logger.debug("in party update, party = %s", party)
        logger.debug("in party update, game = %s", game)
        score1 = request.data.get('score1')
        score2 = request.data.get('score2')
        logger.debug("in party update, score 2= %s", score2)
        duration = request.data.get('duration')
        logger.debug("in party update, duration = %s", duration)
        winner = request.data.get('winner_name')
        user1_id = party.player1.id if party.player1 else None
        logger.debug("in party update, user 1 id = %s", user1_id)
        user2_id = party.player2.id if party.player2 else None
        logger.debug("in party update, user 2 id = %s", user2_id)
        
        #qui a gagner
        if winner == 'player 1':
            win1 = True
            win2 = False
        else:
            win1 = False
            win2 = True

        # une partie dans un tournoi ?
        if request.data.get('type') == 'Matchmaking':
            tour = False    
        else:
            tour = True
            if request.data.get('tour_winner') == 'player 1':
                tour_win1 = True
            else:
                tour_win1 = False
        try:
            userStat1 = UserStatsByGame.objects.get(game=game, user=user1_id)
            userStat1.updateUserData(duration, win1, tour_win1, False, score1)
        except UserStatsByGame.DoesNotExist:
            return Response({"detail": "Player1 not found."}, status=404)
        
        if game == 2 or game == 3:
            try:
                userStat2 = UserStatsByGame.objects.get(game=game, user=user2_id)
                userStat2.updateUserData(duration, win2, tour, False, score2)
            except UserStatsByGame.DoesNotExist:
                return Response({"detail": "Player2 not found."}, status=404)
            
            try:
                status2 = CustomUser.objects.get(id=user2_id)
                status2.updateStatus('online')
            except CustomUser.DoesNotExist:
                return Response({"detail": "Player2 not found."}, status=404)
    
        try:
            status1 = CustomUser.objects.get(id=user1_id)
            status1.updateStatus('online')
        except CustomUser.DoesNotExist:
            return Response({"detail": "Player1 not found."}, status=404)
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

        queryset = self.get_queryset().filter(game=game, player1=user, type='Matchmaking').order_by('date')[:5]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def getTourDataByParty(self, request, pk=None):
        queryset = self.get_queryset()
        party = get_object_or_404(queryset, pk=pk)
        tour = party.tour
        serializer = TournamentSerializer(tour)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def getPlayerUserInfo(self, request, pk=None):
        queryset = self.get_queryset()
        party = get_object_or_404(queryset, pk=pk)
        user2 = party.player2
        serializer = CustomUserSerializer(user2)
        return Response(serializer.data)
    