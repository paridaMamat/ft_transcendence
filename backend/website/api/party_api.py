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