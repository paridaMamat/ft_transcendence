from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from ..models import *
from ..models import Game
from ..serializers import *
from rest_framework import viewsets, status, permissions
from rest_framework.permissions import BasePermission
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
import json
from django.utils import timezone
import math

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request): #POST method
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # Saves the new object
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None): # GET method
        queryset = self.get_queryset()
        game = get_object_or_404(queryset, pk=pk)  # Fetches by primary key
        serializer = self.get_serializer(game)
        return Response(serializer.data)

    def update(self, request, pk=None): # PUT method
        queryset = self.get_queryset()
        game = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(game, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # Updates the existing object
        return Response(serializer.data)

    def leaderboard_data(game, limit=None):
        stat = game.userdatagame_set.order_by('-ratio')
        # if limit:
        #     stat = stat[:limit]
        data = [{"user": s.user.getUserFullInfos(), "stat" : s.getUserDataGame()()} for s in stat]
        return data

    # @login_required
    # @require_http_methods(['GET'])
    # def getLeaderboard(request, id_game):
    #     game = Game.objects.get(id=id_game)
    #     data =  leaderboard_data(game)
    #     return JsonResponse({'status': 'ok', 'users': data})

    # @login_required
    # @require_http_methods(['GET'])
    # def getLeaderboard_length(request, id_game, length):
    #     game = Game.objects.get(id=id_game)
    #     data = leaderboard_data(game, length)
    #     return JsonResponse({'status': 'ok', 'users': data})

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def getLeaderboard(request, pk=None):
        game = get_object_or_404(Game, pk=pk)
        # queryset = leaderboard_data(game, pk)
        queryset = game.getUserDataGame_set.order_by('-ratio') 
        datas = [{"user": s.user.getUserFullInfos(), "stats" : s.getUserDataGame()} for s in queryset]
        serializer = GameSerializer.get_serializer(datas, many=True)
        # return JsonResponse({'status': 'ok', 'users': data})
        return Response(serializer.data)
