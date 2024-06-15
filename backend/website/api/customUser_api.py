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

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser
    
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):  # allow the current user to get his infos via url localhost/api/users/me
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None): # PUT method
        queryset = self.get_queryset()
        user = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # Updates the existing object
        return Response(serializer.data)
    
    def destroy(self, pk=None, *args, **kwargs): # DELETE method
        queryset = self.get_queryset()
        user = get_object_or_404(queryset, pk=pk)
        user.delete()  # Deletes the object
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def update_alias(self, request, pk=None): # PUT method
        queryset = self.get_queryset()
        alias = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(alias, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # Updates the existing object
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def retrieve_top_five(self, request): # GET method
        queryset = self.get_queryset()
        filtered_queryset = queryset.order_by('level')[:5]
        serializer = self.get_serializer(filtered_queryset, many=True)
        return Response(serializer.data)
    

