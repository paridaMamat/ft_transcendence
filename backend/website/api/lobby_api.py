from django.shortcuts import get_object_or_404
from ..models import *
from ..serializers import *
from rest_framework import viewsets, status, permissions
from rest_framework.permissions import BasePermission
from rest_framework.response import Response

class LobbyViewSet(viewsets.ModelViewSet):
    queryset = Lobby.objects.all()
    serializer_class = LobbySerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request): #POST method
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # Saves the new object
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
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

class UserInLobbyViewSet(viewsets.ModelViewSet):
    queryset = UserInLobby.objects.all()
    serializer_class =UserInLobbySerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request): #POST method
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # Saves the new object
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
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