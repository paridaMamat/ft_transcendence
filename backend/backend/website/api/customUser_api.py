from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,  HttpResponse, Http404
from django.shortcuts import get_object_or_404
from ..models import *
from ..serializers import *
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
import logging

logger = logging.getLogger(__name__)

# class IsSuperUser(BasePermission):
#     def has_permission(self, request, view):
#         return request.user and request.user.is_superuser

# def get_http_methods(self, request):
#         # Allow GET, POST, and PUT methods
#         return ['GET', 'POST', 'PUT', 'PATCH']

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_http_methods(self, request):
        # Allow GET, POST, and PUT methods
        return ['GET', 'POST', 'PUT', 'PATCH']

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
    
    @action(detail=True, methods=['patch'])
    def update_friends(self, request, pk=None):
        logger.debug("Received request data: %s", request.data)
        user = self.get_queryset().get(pk=pk)  # Get the user object
        serializer = self.get_serializer(user, data=request.data, partial=True)  # Use user serializer (not friend)

        # Logic for adding or removing friends based on request data
        for friend_id in request.data.get('add_friends', []):
            try:
                friend = CustomUser.objects.get(pk=friend_id)
                user.friends.add(friend)
            except CustomUser.DoesNotExist:
                # Handle friend not found error (optional)
                pass

        for friend_id in request.data.get('remove_friends', []):
            try:
                friend = CustomUser.objects.get(pk=friend_id)
                user.friends.remove(friend)
            except CustomUser.DoesNotExist:
                # Handle friend not found error (optional)
                pass
        serializer.save()  # Save the updated user object
        return Response(serializer.data, status=status.HTTP_200_OK)

