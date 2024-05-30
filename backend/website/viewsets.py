from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *
from rest_framework import viewsets, status, permissions
from rest_framework.permissions import BasePermission
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required

#####################################
#                                   #
#   Django REST Framework ViewSets  #
#                                   #
#####################################

# ---> CustomUser ViewSets

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

# ---> Game ViewSets

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

# ---> Party ViewSets

class PartyViewSet(viewsets.ModelViewSet):
    queryset = Party.objects.all()
    serializer_class = PartySerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request): #POST method
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # Saves the new object
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None): # GET method
        queryset = self.get_queryset()
        party = get_object_or_404(queryset, pk=pk)  # Fetches by primary key
        serializer = self.get_serializer(party)
        return Response(serializer.data)

    def update(self, request, pk=None): # PUT method
        queryset = self.get_queryset()
        party = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(party, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # Updates the existing object
        return Response(serializer.data)

# ---> PartyInTournament ViewSets

class PartyInTournamentViewSet(viewsets.ModelViewSet):
    queryset = PartyInTournament.objects.all()
    serializer_class = PartyInTournamentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request): #POST method
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # Saves the new object
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None): # GET method
        queryset = self.get_queryset()
        tour_party = get_object_or_404(queryset, pk=pk)  # Fetches by primary key
        serializer = self.get_serializer(tour_party)
        return Response(serializer.data)

    def update(self, request, pk=None): # PUT method
        queryset = self.get_queryset()
        tour_party = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(tour_party, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # Updates the existing object
        return Response(serializer.data)

# ---> Lobby ViewSets

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

# ---> UserInLobby ViewSets

class UserInLobbyViewSet(viewsets.ModelViewSet):
    queryset = UserInLobby.objects.all()
    serializer_class = UserInLobbySerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request): #POST method
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # Saves the new object
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        user = request.user  # Fetches by primary key
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None): # PUT method
        queryset = self.get_queryset()
        user = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # Updates the existing object
        return Response(serializer.data)
    
    def destroy(self, request, pk=None, *args, **kwargs): # DELETE method
        queryset = self.get_queryset()
        user = get_object_or_404(queryset, pk=pk)
        user.delete()  # Deletes the object
        return Response(status=status.HTTP_204_NO_CONTENT)

# ---> Tournament ViewSets

class TournamentViewSet(viewsets.ModelViewSet):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = [IsSuperUser]

    def create(self, request): #GET method
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # Saves the new object
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

# ---> UserStats ViewSets

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
        return Response(status=status.HTTP_204_NO_CONTENT)


###############################################
##                                            #
##             UserStats Views                #
##                                            #
###############################################

#class UserStatsByGameViewSet(viewsets.ModelViewSet):
#    queryset = UserStatsByGame.objects.all()
#    serializer_class = UserStatsSerializer
#    permission_classes = [IsSuperUser]

#@api_view(['GET', 'POST'])
#@login_required
#def tournament_info(request):
#    if request.method == 'GET':
#        tour = UserStatsByGame.objects.all()
#        serializer = UserStatsSerializer(tour, many=True)
#        return JsonResponse(serializer.data, safe=False)

#def tournaments_list(request):
#    if request.method == 'POST':
#        serializer = UserStatsSerializer(data=request.data)
#    if serializer.is_valid():
#        serializer.save()
#        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
#    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#@api_view(['GET', 'PUT', 'DELETE'])
#@login_required
#def tournament_detail(request, id):
#    try:
#        tour = UserStatsByGame.objects.get(pk=id)
#    except UserStatsByGame.DoesNotExist:
#        return Response(status=status.HTTP_404_NOT_FOUND)

#    if request.method == 'GET':
#        serializer = UserStatsSerializer(tour)
#        return JsonResponse(serializer.data)

#    elif request.method == 'PUT':
#        serializer = UserStatsSerializer(tour, data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return JsonResponse(serializer.data)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#    elif request.method == 'DELETE':
#        tour.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)

##############################################
##                                           #
##             Game Views                    #
##                                           #
##############################################
   
#class GameViewSet(viewsets.ModelViewSet): #to get infos of all the games ...
#    queryset = Game.objects.all()
#    serializer_class = GameSerializer
#    permission_classes = {IsSuperUser}

#@api_view(['GET'])
#@login_required
#def game_stats(request):  #to get infos of the current game ...
#    game = request.game
#    serializer = GameSerializer(game)
#    return Response(serializer.data, safe=False)

#@api_view(['POST'])
#@login_required
#def games_score(request): #to send game data to the database...
#    serializer = GameSerializer(data=request.data)
#    if serializer.is_valid():
#        serializer.save()
#        return Response(serializer.data, status=status.HTTP_201_CREATED)
#    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#@api_view(['GET', 'PUT', 'DELETE'])
#@login_required
#def game_detail(request, id): 
#    try:
#        game = Game.objects.get(pk=id) #to use/manipulate infos of a chosen game ...
#    except Game.DoesNotExist:
#        return Response(status=status.HTTP_404_NOT_FOUND)

#    if request.method == 'GET':
#        serializer = GameSerializer(game)
#        return Response(serializer.data)

#    elif request.method == 'PUT':
#        serializer = GameSerializer(game, data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#    elif request.method == 'DELETE':
#        game.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)
    
###############################################
##                                            #
##             Party Views                    #
##                                            #
###############################################

#class PartyViewSet(viewsets.ModelViewSet):
#    queryset = Party.objects.all()
#    serializer_class = PartySerializer
#    permission_classes = {IsSuperUser}

#@api_view(['GET'])
#@login_required
#def party_info(request):
#    party = request.party
#    serializer = PartySerializer(party)
#    return JsonResponse(serializer.data, safe=False)

#@api_view(['POST'])
#@login_required
#def parties_list(request):
#    if request.method == 'POST':
#        serializer = PartySerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#@api_view(['GET', 'PUT', 'DELETE'])
#@login_required
#def party_detail(request, id):
#    try:
#        party = Party.objects.get(pk=id)
#    except Party.DoesNotExist:
#        return Response(status=status.HTTP_404_NOT_FOUND)

#    if request.method == 'GET':
#        serializer = PartySerializer(party)
#        return JsonResponse(serializer.data)

#    elif request.method == 'PUT':
#        serializer = PartySerializer(party, data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return JsonResponse(serializer.data)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#    elif request.method == 'DELETE':
#        party.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)

#class PartyInTournamentViewSet(viewsets.ModelViewSet):
#    queryset = PartyInTournament.objects.all()
#    serializer_class = PartyInTournamentSerializer
#    permission_classes = {IsSuperUser}

#@api_view(['GET'])
#@login_required
#def party_tour_info(request):
#    party = request.party
#    serializer = PartySerializer(party)
#    return JsonResponse(serializer.data, safe=False)

#@api_view(['POST'])
#@login_required
#def parties_tour_list(request):
#    if request.method == 'POST':
#        serializer = PartyInTournamentSerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#@api_view(['GET', 'PUT', 'DELETE'])
#@login_required
#def party_tour_detail(request, id):
#    try:
#        user = PartyInTournament.objects.get(pk=id)
#    except PartyInTournament.DoesNotExist:
#        return Response(status=status.HTTP_404_NOT_FOUND)

#    if request.method == 'GET':
#        serializer = PartyInTournamentSerializer(user)
#        return JsonResponse(serializer.data)

#    elif request.method == 'PUT':
#        serializer = PartyInTournamentSerializer(user, data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return JsonResponse(serializer.data)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#    elif request.method == 'DELETE':
#        user.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)

###############################################
##                                            #
##             Lobby Views                    #
##                                            #
###############################################


#class LobbyViewSet(viewsets.ModelViewSet):
#    queryset = Lobby.objects.all()
#    serializer_class = LobbySerializer
#    permission_classes = {IsSuperUser}

#@api_view(['GET'])
#@login_required
#def lobby_info(request):
#    if request.method == 'GET':
#        lobby = request.game
#        serializer = LobbySerializer(lobby)
#        return JsonResponse(serializer.data, safe=False)

#@api_view(['POST'])
#@login_required
#def Lobbies_list(request):
#    if request.method == 'POST':
#        serializer = LobbySerializer(data=request.data)
#    if serializer.is_valid():
#        serializer.save()
#        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
#    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#@api_view(['GET', 'PUT', 'DELETE'])
#@login_required
#def lobby_detail(request, id):
#    try:
#        lobby = Lobby.objects.get(pk=id)

#    except Lobby.DoesNotExist:
#        return Response(status=status.HTTP_404_NOT_FOUND)

#    if request.method == 'GET':
#        serializer = LobbySerializer(lobby)
#        return JsonResponse(serializer.data)

#    elif request.method == 'PUT':
#        serializer = LobbySerializer(lobby, data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return JsonResponse(serializer.data)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#    elif request.method == 'DELETE':
#        lobby.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)
    
#class UserInLobbyViewSet(viewsets.ModelViewSet):
#    queryset = UserInLobby.objects.all()
#    serializer_class = UserInLobbySerializer
#    permission_classes = {IsSuperUser}

#@api_view(['GET'])
#@login_required
#def user_in_lobby_info(request):
#    users = UserInLobby.objects.all()
#    serializer = UserInLobbySerializer(users, many=True)
#    return JsonResponse(serializer.data, safe=False)
    
#@api_view(['GET', 'POST'])
#@login_required
#def user_in_lobby_list(request):
#    if request.method == 'POST':
#        serializer = UserInLobbySerializer(data=request.data)
#    if serializer.is_valid():
#        serializer.save()
#        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
#    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#@api_view(['GET', 'PUT', 'DELETE'])
#@login_required
#def user_in_lobby_detail(request, id):
#    try:
#        user = UserInLobby.objects.get(pk=id)
#    except UserInLobby.DoesNotExist:
#        return Response(status=status.HTTP_404_NOT_FOUND)

#    if request.method == 'GET':
#        serializer = UserInLobbySerializer(user)
#        return JsonResponse(serializer.data)

#    elif request.method == 'PUT':
#        serializer = UserInLobbySerializer(user, data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return JsonResponse(serializer.data)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#    elif request.method == 'DELETE':
#        user.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)
    
##################################################
##                                               #
##             Tournament Views                  #
##                                               #
##################################################

#class TournamentViewSet(viewsets.ModelViewSet):
#    queryset = Tournament.objects.all()
#    serializer_class = TournamentSerializer
#    permission_classes = {IsSuperUser}

#@api_view(['GET', 'POST'])
#@login_required
#def tournament_info(request):
#    if request.method == 'GET':
#        tour = Tournament.objects.all()
#        serializer = TournamentSerializer(tour, many=True)
#        return JsonResponse(serializer.data, safe=False)

#def tournaments_list(request):
#    if request.method == 'POST':
#        serializer = TournamentSerializer(data=request.data)
#    if serializer.is_valid():
#        serializer.save()
#        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
#    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#@api_view(['GET', 'PUT', 'DELETE'])
#@login_required
#def tournament_detail(request, id):
#    try:
#        tour = Tournament.objects.get(pk=id)
#    except Tournament.DoesNotExist:
#        return Response(status=status.HTTP_404_NOT_FOUND)

#    if request.method == 'GET':
#        serializer = TournamentSerializer(tour)
#        return JsonResponse(serializer.data)

#    elif request.method == 'PUT':
#        serializer = TournamentSerializer(tour, data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return JsonResponse(serializer.data)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#    elif request.method == 'DELETE':
#        tour.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)
