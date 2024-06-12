from django.contrib.auth import login, logout
from django.db.models import Q
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect, get_object_or_404, reverse
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
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated

######################################################################
#                                                                    #
#                         Django Views                               #
#                                                                    #
######################################################################

class LoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            login(request, user)

            if user.two_factor_enabled:
                # Redirect to OTP verification page
                request.session['temp_user_id'] = user.id
                return Response({'redirect': True, 'url': '#verify_otp'}, status=status.HTTP_200_OK)
            else:
                # Generate JWT tokens if authentication successful
                tokens = get_tokens_for_user(user)
                return Response(tokens, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OTPVerificationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Serve the OTP verification page
        return render(request, 'verify_otp.html')

    def post(self, request):
        otp = request.data.get('otp')
        user_id = request.session.get('temp_user_id')
        
        if not user_id:
            return Response({'error': 'Session expired, please login again.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)

        totp = pyotp.TOTP(user.two_factor_secret)
        if totp.verify(otp):
            # OTP is valid, clear the temporary user session
            del request.session['temp_user_id']
            # Generate JWT tokens
            tokens = get_tokens_for_user(user)
            return Response(tokens, status=status.HTTP_200_OK) # revoir la redir
        else:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(login_required, name='dispatch')
class Enable2FAView(APIView):
    def get(self, request):
        user = request.user
        otp_secret = pyotp.random_base32()
        user.two_factor_secret = otp_secret
        user.two_factor_enabled = True
        user.save()

        # Generate QR code
        otp_auth_url = pyotp.totp.TOTP(otp_secret).provisioning_uri(name=user.username, issuer_name="ft_transcendence")
        qr = qrcode.make(otp_auth_url)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()

        # Set temp_user_id in the session
        request.session['temp_user_id'] = user.id

        return render(request, 'enable_2fa.html', {'qr_code_base64': qr_code_base64, 'otp_secret': otp_secret})
    
class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request):
        user = request.user
        return JsonResponse({'message': 'You are authenticated'})

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
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

def base(request):
    return render(request, "base.html")

@permission_classes([IsAuthenticated])
@login_required
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

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def friends_view(request):
    print("In my firends_views my user is : ", request.user)  # Debugging: Print the current user
    return render(request, 'friends.html')

@permission_classes([IsAuthenticated])
@login_required
def accueil(request):
    return render(request, "accueil.html")

@permission_classes([IsAuthenticated])
@login_required
def about_us_view(request):
    return render(request, "about_us.html")

@permission_classes([IsAuthenticated])
@login_required
def logout_view(request):
    logout(request)
    return redirect('login_view')

@permission_classes([IsAuthenticated])
@login_required
def profil_view(request):
    return render(request, "profil.html")


@permission_classes([IsAuthenticated])
@login_required
def start_AI(request):
    return render(request, "start_AI.html")

def error_view(request):
    return render('error_404.html')














@permission_classes([IsAuthenticated])
# @login_required
# def lobby_view(request):
#     return render(request, "lobby.html")
@login_required
def lobby_view(request, game_id):
    game = Game.objects.get(id=game_id)
    lobby, created = Lobby.objects.get_or_create(game=game)
    user_in_lobby, created = UserInLobby.objects.get_or_create(user=request.user, lobby=lobby)

    # Logique de matchmaking pour trouver un adversaire
    opponent = find_opponent(request.user, lobby)

    context = {
        'lobby': lobby,
        'user_in_lobby': user_in_lobby,
        'opponent': opponent,

    }
    return render(request, 'lobby.html', context)


def find_opponent(user, lobby):
    user_level = user.level
    max_level_diff = 1

    while True:
        level_range = (
            Q(level__gte=user_level - max_level_diff) &
            Q(level__lte=user_level + max_level_diff)
        )
        opponents = CustomUser.objects.filter(
            level_range,
            userinlobby__lobby=lobby,
            userinlobby__status='waiting'
        ).exclude(id=user.id).order_by('?')

        if opponents.exists():
            return opponents.first()

        max_level_diff += 1
        if max_level_diff > 5:
            return None


def check_opponent(request):
    if request.is_ajax():
        user_in_lobby = UserInLobby.objects.get(user=request.user)
        opponent = user_in_lobby.get_opponent()
        if opponent:
            opponent_data = {
                'username': opponent.username,
                'avatar': opponent.avatar.url,
            }
            return JsonResponse({'opponent': opponent_data})
        else:
            return JsonResponse({'opponent': None})
    else:
        return JsonResponse({'error': 'Requête non autorisée'}, status=400)


# @login_required
# def enter_lobby(request):
#     game = get_object_or_404(Game)
#     user = request.user
#     print(f"User {user.username} entering lobby for game {game.id}")  # Log

#     # Ajouter l'utilisateur au lobby
#     lobby, created = Lobby.objects.get_or_create(game=game)
#     lobby.users.add(user)
#     user.is_waiting = True
#     user.save()

#     # Chercher un adversaire
#     potential_opponents = CustomUser.objects.filter(is_waiting=True, level__range=(user.level-1, user.level+1)).exclude(id=user.id)
#     print(f"Potential opponents found: {potential_opponents.count()}")  # Log
    
#     if potential_opponents.exists():
#         opponent = potential_opponents.first()
#         print(f"Match found: {opponent.username}")  # Log
        
#         # Créer une partie
#         party = Party.objects.create(
#             game=game,
#             game_name=game,
#             player1=user,
#             player2=opponent,
#             status='waiting'
#         )

#         # Mettre à jour les états des utilisateurs
#         user.is_waiting = False
#         opponent.is_waiting = False
#         user.save()
#         opponent.save()
        
#         lobby.users.remove(user)
#         lobby.users.remove(opponent)

#         # Retourner les informations de l'adversaire
#         return JsonResponse({
#             'status': 'matched',
#             'opponent': {
#                 'username': opponent.username,
#                 'avatar': opponent.avatar.url,
#                 'level': opponent.level
#             },
#             'party_id': party.id,
#             'game_name': game.game_name
#         })
    
#     print("No match found, user still waiting...")  # Log
#     return JsonResponse({'status': 'waiting'})


# @permission_classes([IsAuthenticated])
# @login_required
# def start_game(request, game_name):
#     if game_name == 'pong':
#         return render(request, "pong3D.html")
#     elif game_name == 'memory':
#         return render(request, "memory_game.html")

# class MatchmakingView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         game_type = request.data.get('game')
        
#         # Check if the user is already in a lobby
#         existing_user_lobby = UserInLobby.objects.filter(user=request.user).first()
#         if existing_user_lobby:
#             return JsonResponse({'message': 'You are already in a lobby', 'lobby_id': existing_user_lobby.lobby.id})

#         # Check for an available lobby for the specific game type
#         available_lobby = Lobby.objects.filter(game=game_type, users__lt=2).first()
        
#         if available_lobby:
#             # Add user to the lobby
#             UserInLobby.objects.create(user=request.user, lobby=available_lobby)
#             if available_lobby.users.count() == 2:
#                 return JsonResponse({'message': 'Match found! Starting the game.', 'lobby_id': available_lobby.id})
#             return JsonResponse({'message': 'Waiting for another player.', 'lobby_id': available_lobby.id})
        
#         # No available lobby, create a new one
#         new_lobby = Lobby.objects.create(game=game_type)
#         UserInLobby.objects.create(user=request.user, lobby=new_lobby)
#         return JsonResponse({'message': 'Lobby created. Waiting for another player.', 'lobby_id': new_lobby.id})

#     def delete(self, request):
#         # Find the user in the lobby
#         user_lobby = UserInLobby.objects.filter(user=request.user).first()
#         if user_lobby:
#             user_lobby.delete()
#             return JsonResponse({'message': 'You have left the lobby'})
#         return JsonResponse({'message': 'You are not in any lobby'})