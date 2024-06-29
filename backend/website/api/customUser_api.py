from django.http import JsonResponse,  HttpResponse, Http404
from django.shortcuts import get_object_or_404
from ..models import *
from ..serializers import *
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
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

    
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_friends(self, request, pk=None):
        logger.debug(f"User authenticated: {request.user.is_authenticated}")
        logger.debug(f"User ID: {request.user.id}")
        logger.debug(f"Requested user ID: {pk}")
        logger.debug("Received request data: %s", request.data)
        user = self.get_queryset().get(pk=pk)  # Get the user object
        friend_id = request.data.get('friendId')

        if not friend_id:
            return Response({'status': 'error', 'message': 'friendId is required.'}, status=400)

        if int(friend_id) == user.id:
            return Response({'status': 'error', 'message': 'You cannot add yourself as a friend.'}, status=400)

        try:
            new_friend = CustomUser.objects.get(pk=friend_id)
            logger.debug("new_friend: %s", new_friend)
        except CustomUser.DoesNotExist:
            return Response({'status': 'error', 'message': 'This user does not exist.'}, status=404)

        if new_friend in user.friends.all():
            return Response({'status': 'error', 'message': 'This user is already your friend.'}, status=400)

        user.friends.add(new_friend)
        return Response({'status': 'ok', 'message': 'Friend added successfully.'})
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def remove_friends(self, request, pk=None):
        logger.debug(f"User authenticated: {request.user.is_authenticated}")
        logger.debug(f"User ID: {request.user.id}")
        logger.debug(f"Requested user ID: {pk}")
        logger.debug("Received request data: %s", request.data)
        user = self.get_queryset().get(pk=pk)  # Get the user object
        friend_id = request.data.get('friendId')

        if not friend_id:
            return Response({'status': 'error', 'message': 'friendId is required.'}, status=400)

        if int(friend_id) == user.id:
            return Response({'status': 'error', 'message': 'You cannot remove yourself.'}, status=400)

        try:
            old_friend = CustomUser.objects.get(pk=friend_id)
            logger.debug("old_friend: %s", old_friend)
        except CustomUser.DoesNotExist:
            return Response({'status': 'error', 'message': 'This user does not exist.'}, status=404)

        if old_friend in user.friends.all():
            user.friends.remove(old_friend)
            return Response({'success': True, 'message': 'Friend remove successfully.'})
    
    @action(detail=False, methods=['get'])
    def retrieve_friends_data(self, request, pk=None):
        try:
            logger.debug(f"Requested user ID: {pk}")
            logger.debug("Received request data: %s", request.data)
            user = request.user
            list_friend = user.getFriends()
            data = list_friend
            return Response({'status': 'ok', 'friend_request': data})
        except CustomUser.DoesNotExist:
            return Response({'status': 'error', 'message': 'This user does not exist.'}, status=404)

        # if not friend_id:
        #     return Response({'status': 'error', 'message': 'friendId is required.'}, status=400)

        # if int(friend_id) == user.id:
        #     return Response({'status': 'error', 'message': 'You cannot remove yourself.'}, status=400)

        # try:
        #     old_friend = CustomUser.objects.get(pk=friend_id)
        #     logger.debug("old_friend: %s", old_friend)
        # except CustomUser.DoesNotExist:
        #     return Response({'status': 'error', 'message': 'This user does not exist.'}, status=404)

        # if old_friend in user.friends.all():
        #     return Response({'status': 'error', 'message': 'This user is already your friend.'}, status=400)

        # user.friends.remove(old_friend)
        # return Response({'status': 'ok', 'message': 'Friend added successfully.'})

    # def retrieve(self, request, pk=None): # GET method
    #     queryset = self.get_queryset()
    #     game = get_object_or_404(queryset, pk=pk)  # Fetches by primary key
    #     serializer = self.get_serializer(game)
    #     return Response(serializer.data)
