# views.py
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.http import JsonResponse,  HttpResponse, Http404
from .models import CustomUser
from .serializers import *
from rest_framework.response import Response
from rest_framework import status, viewsets, generics
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from website.views import IsSuperUser
import requests

#---------------------------------------------
# Game
#---------------------------------------------

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = {IsSuperUser}
    
#@api_view(['GET', 'POST'])
#def game_list(request):
#    if request.method == 'GET':
#        users = Game.objects.all()
#        serializer = GameSerializer(users, many=True)
#        return JsonResponse(serializer.data, safe=False)

#    elif request.method == 'POST':
#        serializer = GameSerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#@api_view(['GET', 'PUT', 'DELETE'])
#def game_detail(request, id):
#    try:
#        user = Game.objects.get(pk=id)
#    except Game.DoesNotExist:
#        return Response(status=status.HTTP_404_NOT_FOUND)

#    if request.method == 'GET':
#        serializer = GameSerializer(user)
#        return Response(serializer.data)

#    elif request.method == 'PUT':
#        serializer = GameSerializer(user, data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#    elif request.method == 'DELETE':
#        user.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)

#---------------------------------------------
# Party
#---------------------------------------------

class PartyViewSet(viewsets.ModelViewSet):
    queryset = Party.objects.all()
    serializer_class = PartySerializer
    permission_classes = {IsSuperUser}

#@api_view(['GET', 'POST'])
#def party_list(request):
#    if request.method == 'GET':
#        users = Party.objects.all()
#        serializer = PartySerializer(users, many=True)
#        return JsonResponse(serializer.data, safe=False)

#    elif request.method == 'POST':
#        serializer = PartySerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#@api_view(['GET', 'PUT', 'DELETE'])
#def party_detail(request, id):
#    try:
#        user = Party.objects.get(pk=id)
#    except Party.DoesNotExist:
#        return Response(status=status.HTTP_404_NOT_FOUND)

#    if request.method == 'GET':
#        serializer = PartySerializer(user)
#        return Response(serializer.data)

#    elif request.method == 'PUT':
#        serializer = PartySerializer(user, data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#    elif request.method == 'DELETE':
#        user.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)

class PartyStatsViewSet(viewsets.ModelViewSet):
    queryset = PartyStats.objects.all()
    serializer_class = PartyStatsSerializer
    permission_classes = {IsSuperUser}

#@api_view(['GET', 'POST'])
#def party_stats_list(request):
#    if request.method == 'GET':
#        users = PartyStats.objects.all()
#        serializer = PartyStatsSerializer(users, many=True)
#        return JsonResponse(serializer.data, safe=False)

#    elif request.method == 'POST':
#        serializer = PartyStatsSerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#@api_view(['GET', 'PUT', 'DELETE'])
#def party_stats_detail(request, id):
#    try:
#        user = PartyStats.objects.get(pk=id)
#    except PartyStats.DoesNotExist:
#        return Response(status=status.HTTP_404_NOT_FOUND)

#    if request.method == 'GET':
#        serializer = PartyStatsSerializer(user)
#        return Response(serializer.data)

#    elif request.method == 'PUT':
#        serializer = PartyStatsSerializer(user, data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#    elif request.method == 'DELETE':
#        user.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)

#---------------------------------------------
# Lobby
#---------------------------------------------

class LobbyViewSet(viewsets.ModelViewSet):
    queryset = Lobby.objects.all()
    serializer_class = LobbySerializer
    permission_classes = {IsSuperUser}

#@api_view(['GET', 'POST'])
#def lobby_list(request):
#    if request.method == 'GET':
#        users = Lobby.objects.all()
#        serializer = LobbySerializer(users, many=True)
#        return JsonResponse(serializer.data, safe=False)

#    elif request.method == 'POST':
#        serializer = LobbySerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#@api_view(['GET', 'PUT', 'DELETE'])
#def lobby_detail(request, id):
#    try:
#        user = Lobby.objects.get(pk=id)
#    except Lobby.DoesNotExist:
#        return Response(status=status.HTTP_404_NOT_FOUND)

#    if request.method == 'GET':
#        serializer = LobbySerializer(user)
#        return Response(serializer.data)

#    elif request.method == 'PUT':
#        serializer = LobbySerializer(user, data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#    elif request.method == 'DELETE':
#        user.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)
    
class UserInLobby(viewsets.ModelViewSet):
    queryset = UserInLobby.objects.all()
    serializer_class = UserInLobbySerializer
    permission_classes = {IsSuperUser}

#@api_view(['GET', 'POST'])
#def user_in_lobby_list(request):
#    if request.method == 'GET':
#        users = UserInLobby.objects.all()
#        serializer = UserInLobbySerializer(users, many=True)
#        return JsonResponse(serializer.data, safe=False)

#    elif request.method == 'POST':
#        serializer = UserInLobbySerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#@api_view(['GET', 'PUT', 'DELETE'])
#def user_in_lobby_detail(request, id):
#    try:
#        user = UserInLobby.objects.get(pk=id)
#    except UserInLobby.DoesNotExist:
#        return Response(status=status.HTTP_404_NOT_FOUND)

#    if request.method == 'GET':
#        serializer = UserInLobbySerializer(user)
#        return Response(serializer.data)

#    elif request.method == 'PUT':
#        serializer = UserInLobbySerializer(user, data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#    elif request.method == 'DELETE':
#        user.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)
    
#---------------------------------------------
# tournament
#---------------------------------------------

class TournamentViewSet(viewsets.ModelViewSet):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = {IsSuperUser}

#@api_view(['GET', 'POST'])
#def tournament_list(request):
#    if request.method == 'GET':
#        users = Tournament.objects.all()
#        serializer = TournamentSerializer(users, many=True)
#        return JsonResponse(serializer.data, safe=False)

#    elif request.method == 'POST':
#        serializer = TournamentSerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#@api_view(['GET', 'PUT', 'DELETE'])
#def tournament_detail(request, id):
#    try:
#        user = Tournament.objects.get(pk=id)
#    except Tournament.DoesNotExist:
#        return Response(status=status.HTTP_404_NOT_FOUND)

#    if request.method == 'GET':
#        serializer = TournamentSerializer(user)
#        return Response(serializer.data)

#    elif request.method == 'PUT':
#        serializer = TournamentSerializer(user, data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#    elif request.method == 'DELETE':
#        user.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)