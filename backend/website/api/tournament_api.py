from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from ..models import *
from ..serializers import *
from .customUser_api import IsSuperUser
from rest_framework import viewsets, status, permissions
from rest_framework.permissions import BasePermission
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
import json
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
import math

# Définissez le logger pour ce module
import logging

logger = logging.getLogger(__name__)

class TournamentViewSet(viewsets.ModelViewSet):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        logger.debug("Received request data: %s", request.data)
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            logger.error("Validation errors: %s", e.detail)
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        logger.debug("Tournament created successfully")
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None): # GET method
        queryset = self.get_queryset()
        tour = get_object_or_404(queryset, pk=pk)  # Fetches by primary key
        serializer = self.get_serializer(tour)
        return Response(serializer.data)

    def update(self, request, pk=None): # PUT method
        queryset = self.get_queryset()
        tour = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(tour, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # Updates the existing object
        return Response(serializer.data)
    
