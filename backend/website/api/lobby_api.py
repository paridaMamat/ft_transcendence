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

class LobbyViewSet(viewsets.ModelViewSet):
    queryset = Lobby.objects.all()
    serializer_class = LobbySerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['post'], detail=False)
    def create_lobby(self, request):
        serializer = LobbySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            lobby = serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    @action(methods=['post'], detail=False)
    def invite_player_to_lobby(self, request):
        # Logique pour trouver un joueur disponible basé sur les critères de matchmaking
        # Par exemple, trouver un joueur dont le niveau correspond aux exigences du lobby
        lobby = self.get_object()
        available_user = CustomUser.objects.filter(available=True, level__gte=lobby.min_level).order_by('-level').first()
        
        if available_user:
            # Créer une instance de UserInLobby pour lier le joueur au lobby
            UserInLobby.objects.create(user=available_user, lobby=lobby)
            
            return Response({"message": "Un joueur a été invité à rejoindre le lobby."}, status=200)
        else:
            return Response({"error": "Aucun joueur disponible correspondant aux critères de niveau."}, status=400)


    @action(methods=['post'], detail=True)
    def join_lobby(self, request, pk=None):
        lobby = self.get_object()
        user_in_lobby, created = UserInLobby.objects.get_or_create(
            user=request.user,
            lobby=lobby,
            defaults={'status': 'joined'}
        )
        return Response({"message": "Joueur ajouté au lobby."})

    @action(methods=['post'], detail=True)
    def quit_lobby(self, request, pk=None):
        lobby = self.get_object()
        try:
            user_in_lobby = UserInLobby.objects.get(user=request.user, lobby=lobby)
            user_in_lobby.delete()
            return Response({"message": "Joueur retiré du lobby."})
        except UserInLobby.DoesNotExist:
            return Response({"error": "L'utilisateur n'est pas dans ce lobby."}, status=400)

    

    # def create(self, request): #POST method
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()  # Saves the new object
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None): # GET method
        queryset = self.get_queryset()
        users = get_object_or_404(queryset, pk=pk)  # Fetches by primary key
        serializer = self.get_serializer(users)
        return Response(serializer.data)

    def update(self, request, pk=None): # PUT method
        queryset = self.get_queryset()
        users = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(users, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # Updates the existing object
        return Response(serializer.data)
    
    def destroy(self, request, pk=None, *args, **kwargs): # DELETE method
        queryset = self.get_queryset()
        users = get_object_or_404(queryset, pk=pk)
        users.delete()  # Deletes the object
        return Response(status=status.HTTP_204_NO_CONTENT)
    
