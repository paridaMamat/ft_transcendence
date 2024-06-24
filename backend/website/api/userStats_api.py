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
# from .customUser_api import IsSuperUser
# from .customUser_api import IsSuperUser
from django.utils import timezone
import math
import logging

logger = logging.getLogger(__name__)
import logging

logger = logging.getLogger(__name__)

class UserStatsViewSet(viewsets.ModelViewSet):
    queryset = UserStatsByGame.objects.all()
    serializer_class = UserStatsSerializer
    permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request): #POST method
        logger.debug("Received request data: %s", request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # Saves the new object
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        logger.debug("Received request data: %s", request.data)
        user = request.user
        logger.debug("Received request data: %s", request.data)
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def retrieve(self, request, pk=None): # GET method
        logger.debug("Received request data: %s", request.data)
        logger.debug("Received request data: %s", request.data)
        queryset = self.get_queryset()
        stats = get_object_or_404(queryset, pk=pk)  # Fetches by primary key
        serializer = self.get_serializer(stats)
        return Response(serializer.data)

    def update(self, request, pk=None): # PUT method
        logger.debug("Received request data: %s", request.data)
        logger.debug("Received request data: %s", request.data)
        queryset = self.get_queryset()
        stats = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(stats, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # Updates the existing object
        return Response(serializer.data)
    
    def destroy(self, request, pk=None, *args, **kwargs): # DELETE method
        logger.debug("Received request data: %s", request.data)
        logger.debug("Received request data: %s", request.data)
        queryset = self.get_queryset()
        stats = get_object_or_404(queryset, pk=pk)
        stats.delete()  # Deletes the object
        return Response(status=status.HTTP_204_NO_CONTENT)
      
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def retrieveTopFive(self, request, game_id=None):
        logger.debug("Received request data: %s", request.data)
        if not game_id:
            return Response({"detail": "game_id URL parameters are required."}, status=400)
        game = get_object_or_404(Game, id=game_id)
        queryset = UserStatsByGame.objects.filter(game=game).order_by('level')[:5]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def retrieveMyBoard(self, request, game_id=None):
        logger.debug("Received request data: %s", request.data)
        if not game_id:
            return Response({"detail": "Both game_id and user_id URL parameters are required."}, status=400)
        game = get_object_or_404(Game, id=game_id)
        user = request.user
        queryset = self.get_queryset().filter(game=game, user=user)
        if not queryset.exists():
            return Response({"detail": "No stats found for the specified game and user."}, status=404)
        serializer = self.get_serializer(queryset, many=True)
      
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def retrieveTopFive(self, request, game_id=None):
        logger.debug("Received request data: %s", request.data)
        if not game_id:
            return Response({"detail": "game_id URL parameters are required."}, status=400)
        game = get_object_or_404(Game, id=game_id)
        queryset = UserStatsByGame.objects.filter(game=game).order_by('level')[:5]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def retrieveMyBoard(self, request, game_id=None):
        logger.debug("Received request data: %s", request.data)
        if not game_id:
            return Response({"detail": "Both game_id and user_id URL parameters are required."}, status=400)
        game = get_object_or_404(Game, id=game_id)
        user = request.user
        queryset = self.get_queryset().filter(game=game, user=user)
        if not queryset.exists():
            return Response({"detail": "No stats found for the specified game and user."}, status=404)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)