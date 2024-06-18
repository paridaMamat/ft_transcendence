from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse,  HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from .utils import verify_otp, get_tokens_for_user
from django.utils.decorators import method_decorator
import pyotp
import qrcode
import base64
from io import BytesIO
from .models import *
from .serializers import *
from .api import *
import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated

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
    serializer_class = FullUserSerializer
    permission_classes = {IsSuperUser}

    def create(self, request): #POST method
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # Saves the new object
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None): # GET method
        queryset = self.get_queryset()
        user = get_object_or_404(queryset, pk=pk)  # Fetches by primary key
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

# ---> Game ViewSets

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = {IsSuperUser}

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
    permission_classes = {IsSuperUser}

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
    permission_classes = {IsSuperUser}

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
    permission_classes = {IsSuperUser}

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
    permission_classes = {IsSuperUser}

    def create(self, request): #POST method
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # Saves the new object
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None): # GET method
        queryset = self.get_queryset()
        user = get_object_or_404(queryset, pk=pk)  # Fetches by primary key
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
    permission_classes = {IsSuperUser}

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
    permission_classes = {IsSuperUser}

    def create(self, request): #GET method
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # Saves the new object
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
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

#@api_view(['GET', 'POST'])
#def user_list(request):
#    if request.method == 'GET':
#        users = CustomUser.objects.all()
#        serializer = CustomUserSerializer(users, many=True)
#        return JsonResponse(serializer.data, safe=False)

#    elif request.method == 'POST':
#        serializer = CustomUserSerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#@api_view(['GET'])
#@login_required
#def user_info(request):
#    user = request.user
#    serializer = UserRegistrationSerializer(user)
#    return JsonResponse(serializer.data, safe=False)
    
#@api_view(['GET', 'PUT', 'DELETE'])
#@login_required
#def user_detail(request, id):
#    try:
#        user = CustomUser.objects.get(pk=id)
#    except CustomUser.DoesNotExist:
#        return JsonResponse(status=status.HTTP_404_NOT_FOUND)

#    if request.method == 'GET':
#        serializer = UserRegistrationSerializer(user)
#        return JsonResponse(serializer.data)

#    elif request.method == 'PUT':
#        serializer = UserRegistrationSerializer(user, data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return JsonResponse(serializer.data)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#    elif request.method == 'DELETE':
#        user.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)

#####################################
#                                   #
#           Django Views            #
#                                   #
#####################################

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'success': True}) # Send a success response
            else:
                return Response({'error': 'Username or password is incorrect.'}, status=400) # Send an error response
        else:
            return Response({'error': 'Form is invalid.', 'form_errors': form.errors}, status=400)
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login_view')

@renderer_classes([JSONRenderer]) 
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            if CustomUser.objects.filter(username=username).exists():
                return JsonResponse({'status': 'error', 'message': 'This username is already taken.'}, status=400)
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            if CustomUser.objects.filter(email=email).exists():
                return JsonResponse({'status': 'error', 'message': 'This email is already taken.'}, status=400)
            pwd = request.POST.get('password1')
            two_factors_enabled = request.POST.get('two_factors_enabled')
            user = form.save()  # This line assigns the user instance to the 'user' variable
            login(request, user)  # Now 'user' is defined and can be used here
            #redirect_url = reverse('login',args=['login'])
            #return redirect('login')
            if user.two_factor_enabled :
                return JsonResponse({'success': True, 'redirect_url': ('#enable_2fa')})
            else:
                return JsonResponse({'success': True, 'redirect_url': ('#login')})
        else:
            return JsonResponse({'error': form.errors}, status=status.HTTP_400_BAD_REQUEST)
        #else:
        #    return JsonResponse({'error': form.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

@permission_classes([IsAuthenticated])
@login_required
def account_settings(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        # Mettre à jour les informations de l'utilisateur
        user = request.user # Access the currently logged-in user
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        # Rediriger l'utilisateur vers la page d'accueil
        return redirect('#accueil')

    # Récupérer les informations de l'utilisateur actuel pour pré-remplir le formulaire
    user = request.user
    context = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
    }
    return render(request, 'account_settings.html', context)

@permission_classes([IsAuthenticated])
@login_required
def lobby_view(request):
    return render(request, 'lobby.html')

def base(request):
    return render(request, "base.html")

def index(request):
    return render(request, "index.html")

@permission_classes([IsAuthenticated])
@login_required 
def connection(request):
    return render(request, "connection.html")

@permission_classes([IsAuthenticated])
@login_required
def games_view(request):
    return render(request, "games_page.html")

@permission_classes([IsAuthenticated])
@login_required
def AI_view(request):
    return render(request, "AI.html")

@permission_classes([IsAuthenticated])
@login_required
def pong3D(request):
    return render(request, "pong3D.html")

@permission_classes([IsAuthenticated])
@login_required
def memory_game(request):
    return render(request, "memory_game.html")

###############################################
##                                            #
##             UserStats Views                #
##                                            #
###############################################

#class UserStatsByGameViewSet(viewsets.ModelViewSet):
#    queryset = UserStatsByGame.objects.all()
#    serializer_class = UserStatsSerializer
#    permission_classes = {IsSuperUser}

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