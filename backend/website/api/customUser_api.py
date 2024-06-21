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
import logging

logger = logging.getLogger(__name__)

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser
    
    
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_http_methods(self, request):
        # Allow GET, POST, and PUT methods
        return ['GET', 'POST', 'PUT', 'PATCH']
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):  # allow the current user to get his infos via url localhost/api/users/me
        logger.debug("Received request data ME: %s", request.data)
        user = request.user
        serializer = self.get_serializer(user)
        logger.debug("current user data successfully get")
        return Response(serializer.data)

    def update(self, request, pk=None): # PUT / PATCH method
        logger.debug("Received request data PUT/PATCH: %s", request.data)
        queryset = self.get_queryset()
        user = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(user, data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            logger.error("Validation errors: %s", e.detail)
        serializer.save()  # Updates the existing object
        logger.debug("user's data updated successfully")
        return Response(serializer.data)
    
    def destroy(self, pk=None, *args, **kwargs): # DELETE method
        queryset = self.get_queryset()
        user = get_object_or_404(queryset, pk=pk)
        user.delete()  # Deletes the object
        logger.debug("user deleted successfully")
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def update_alias(self, request, pk=None):
        logger.debug("Received request: %s", request.data)
        queryset = self.get_queryset()
        try:
            alias = get_object_or_404(queryset, pk=pk)
            serializer = self.get_serializer(alias, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Exception as e:
            logger.error("Error: %s", e)
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # @action(detail=True, methods=['PATCH'])
    # def update_friends(self, request, pk=None):
    #     logger.debug("Received request data: %s", request.data)
    #     queryset = self.get_queryset()
    #     try:
    #         friends = get_object_or_404(queryset, pk=pk)
    #         serializer = self.get_serializer(friends, data=request.data, partial=True)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #     except Exception as e:
    #         logger.error("Error: %s", e)
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    
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
        #     if not friend_username:
        #         return Response({"error": "Missing 'username' in request data"}, status=status.HTTP_400_BAD_REQUEST)

        #     friend = get_object_or_404(CustomUser, username=friend_username)
            
        #     if friend == user:
        #         return Response({"error": "Cannot add yourself as a friend"}, status=status.HTTP_400_BAD_REQUEST)
            
        #     if not user.friends.filter(pk=friend.pk).exists():
        #         user.friends.add(friend)
        #         user.save()
        #         message = "Friend added successfully"
        #     else:
        #         message = "User is already a friend"

        #     serializer = CustomUserSerializer(user)
        #     return Response({"message": message, "user": serializer.data})
        
        # except Exception as e:
        #     logger.error(f"Error updating friends: {str(e)}")
        #     return Response({"error": "An error occurred while updating friends"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
