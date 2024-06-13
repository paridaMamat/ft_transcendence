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
from .customUser_api import IsSuperUser
from django.utils import timezone
import math

class UserStatsViewSet(viewsets.ModelViewSet):
    queryset = UserStatsByGame.objects.all()
    serializer_class = UserStatsSerializer
    permission_classes = [IsSuperUser]

    def create(self, request): #GET method
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # Saves the new object
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        user = request.user  # Fetches by primary key
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def retrieve(self, request, pk=None): # GET method
        queryset = self.get_queryset()
        stats = get_object_or_404(queryset, pk=pk)  # Fetches by primary key
        serializer = self.get_serializer(stats)
        return Response(serializer.data)

    def update(self, request, pk=None): # PUT method
        queryset = self.get_queryset()
        stats = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(stats, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # Updates the existing object
        return Response(serializer.data)
    
    def destroy(self, request, pk=None, *args, **kwargs): # DELETE method
        queryset = self.get_queryset()
        stats = get_object_or_404(queryset, pk=pk)
        stats.delete()  # Deletes the object
<<<<<<< HEAD
        return Response(status=status.HTTP_204_NO_CONTENT)
=======
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def retrieve5first(self, request): # GET method
        queryset = self.get_queryset()
        filtered_queryset = queryset.order_by('level')[:5]
        # Pas besoin de get_object_or_404 ici car nous ne récupérons pas un objet unique
        serializer = self.get_serializer(filtered_queryset, many=True)
        return Response(serializer.data)
>>>>>>> origin/new_Hinda
