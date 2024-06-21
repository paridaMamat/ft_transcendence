from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm , CustomUserUpdateForm
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse,  HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from .utils import verify_otp, get_tokens_for_user
from django.utils.decorators import method_decorator
from django.utils import translation
from django.utils.translation import gettext_lazy as _
import pyotp
import qrcode
import base64
from io import BytesIO
from .models import *
from .serializers import *
from .api import *
import requests
from decimal import Decimal
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages

######################################################################
#                                                                    #
#                         Django Views                               #
#                                                                    #
######################################################################

class LoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # if request.user.is_authenticated:
        #     return redirect('accueil.html')
        return render(request, 'login.html')

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            if (user.status == 'offline'):
                user.status = 'online'
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
    print("In my account_settings my user is : ", request.user)  # Debugging: Print the current user
    if request.method == 'POST':
        user_form = CustomUserUpdateForm(request.POST, request.FILES, instance=request.user)
        password_form = PasswordChangeForm(request.user, request.POST)

        if 'password_change' in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Votre mot de passe a été mis à jour avec succès!')
                JsonResponse({'success': True, 'redirect_url': ('#account_settings')})
            else:
                messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')

        elif user_form.is_valid():
            user = user_form.save()
            messages.success(request, 'Vos informations ont été mises à jour avec succès!')
            JsonResponse({'success': True, 'redirect_url': ('#account_settings')})
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')

    else:
        user_form = CustomUserUpdateForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)

    context = {
        'user_form': user_form,
        'password_form': password_form,
    }
    return render(request, 'account_settings.html', context)

def base(request):
    return render(request, "base.html")

# def set_language(request):
#     user_language = request.GET.get('language', 'fr')
#     # user_language = request.GET.get('language', settings.LANGUAGE_CODE)
#     translation.activate(user_language)
#     response = redirect(request.META.get('HTTP_REFERER', '/'))
#     response.set_cookie(settings.LANGUAGE_COOKIE_NAME, user_language)
#     return response

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

# @permission_classes([IsAuthenticated])
# @login_required
# def lobby_view(request):
#     return render(request, "lobby.html")

@permission_classes([IsAuthenticated])
@login_required
def start_AI(request):
    return render(request, "start_AI.html")

@permission_classes([IsAuthenticated])
@login_required
def lobby_tournoi_view(request):
    return render(request, "lobby_tournoi.html")

@permission_classes([IsAuthenticated])
@login_required
def lobby_partie_view(request):
    return render(request, "lobby_partie.html")

@permission_classes([AllowAny])
def error_view(request):
    return render(request, "error_404.html")

def test_view(request):
    return render(request, "test.html")

@permission_classes([IsAuthenticated])
@login_required
def create_tournament_view(request):
    tournament_id = request.GET.get('id')
    return render(request, "createTournament.html", {'tournament_id': tournament_id})

@permission_classes([IsAuthenticated])
@login_required
def page_finale_view(request):
    return render(request, "page_finale.html")

@permission_classes([IsAuthenticated])
@login_required
def choix1_view(request):
    return render(request, "choix1.html")

@permission_classes([IsAuthenticated])
@login_required
def choix2_view(request):
    return render(request, "choix2.html")

def set_language(request):
    user_language = request.GET.get('language', 'fr')
    translation.activate(user_language)
    request.session[translation.LANGUAGE_SESSION_KEY] = user_language
    # Récupérez vos nouvelles traductions ici.
    translations = {
        'Home': str(_("Home")),
        'Languages': str(_("Languages")),
        'Logout': str(_("Logout")),
        'French': str(_("French")),
        'English': str(_("English")),
        'Uyghur': str(_("Uyghur")),
        'Arabic': str(_("Arabic")),
    }
    return JsonResponse(translations)



###########################
##                       ##
##   Looby matchmaking   ##
##                       ##
###########################


import logging

# Définissez le logger pour ce module
logger = logging.getLogger(__name__)

class LobbyView(APIView):
    permission_classes = [IsAuthenticated]

    # def get(self, request):
    #     lobby_id = request.GET.get('id')
    #     logger.info("get lobby view")
    #     return render(request, 'lobby.html', {'id': lobby_id})

    def post(self, request):
        logger.info("post lobby view")
        lobby_id = request.data.get('id')

        game_id = self.get_game_name_by_lobby_id(lobby_id)
        if not game_id:
            logger.error(f"Invalid lobby ID: {lobby_id}")
            return Response({'error': 'Invalid lobby ID'}, status=status.HTTP_400_BAD_REQUEST)
        
        return self.handle_lobby_request(request, game_id)
        
    def handle_lobby_request(self, request, game_id):

        try:
            current_game = Game.objects.get(game_name=game_id)
        except Game.DoesNotExist:
            return Response({'error': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)
        
        lobby, created = Lobby.objects.get_or_create(game=current_game)
        current_user = request.user
        logger.info(f"User {current_user.username} entering lobby for game {game_id} / current_game {current_game.id}")

        lobby.users.add(current_user)
        logger.info(f"User {current_user.username} added to lobby {lobby.id}")
        current_user.status = 'waiting'
        current_user.save()

        current_user_stats, created = UserStatsByGame.objects.get_or_create(user=current_user, game=current_game)
        if created:
            logger.info(f"Created new UserStatsByGame for user {current_user.username} and game {current_game.id}")

        potential_opponents = self.find_potential_opponents(current_user_stats)
        logger.info(f"Potential opponents found: {len(potential_opponents)}")

        if potential_opponents:
            opponent_stats = potential_opponents[0]
            opponent = opponent_stats.user
            logger.info(f"Match found: {opponent.username} with a parties_ratio of {opponent_stats.parties_ratio}")

            lobby.users.add(opponent)

            party = Party.objects.create(
                game=current_game,
                player1=current_user,
                player2=opponent,
                status='waiting'
            )

            current_user.status = 'waiting'
            opponent.status = 'waiting'
            current_user.save()
            opponent.save()

            lobby.users.remove(current_user)
            lobby.users.remove(opponent)

            opponent_data = CustomUserSerializer(opponent).data
            party_data = PartySerializer(party).data

            return Response({
                'status': 'matched',
                'opponent': opponent_data,
                'party': party_data,
                'game': current_game.id
            }, status=status.HTTP_201_CREATED)
        
        logger.info("No match found, user still waiting...")
        return Response({'status': 'waiting'}, status=status.HTTP_200_OK)

    def get_game_name_by_lobby_id(self, lobby_id):
        lobby_game_mapping = {
            '2': 'pong',
            '3': 'memory',
        }
        return lobby_game_mapping.get(lobby_id)
    
    def find_potential_opponents(self, current_user_stats):
        all_stats = UserStatsByGame.objects.filter(game=current_user_stats.game, user__status='online').exclude(user=current_user_stats.user)

        # Sort potential opponents by closeness to current user's parties_ratio
        sorted_opponents = sorted(
            all_stats,
            key=lambda stats: abs(Decimal(stats.parties_ratio) - Decimal(current_user_stats.parties_ratio))
        )
        logger.info(f"Potential opponents sorted by parties_ratio: {sorted_opponents}")

        return sorted_opponents

###########################
##                       ##
##  Tournament Lobby     ##
##                       ##
###########################

class TournamentLobbyView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        lobby_id = request.GET.get('id')
        logger.info("get tournament lobby view")
        return render(request, 'tournament_lobby.html', {'id': lobby_id})

    def post(self, request):
        logger.info("post tournament lobby view")
        lobby_id = request.data.get('id')

        game_id = self.get_game_name_by_lobby_id(lobby_id)
        if not game_id:
            logger.error(f"Invalid lobby ID: {lobby_id}")
            return Response({'error': 'Invalid lobby ID'}, status=status.HTTP_400_BAD_REQUEST)
        
        return self.handle_tournament_request(request, game_id)
        
    def handle_tournament_request(self, request, game_id):
        try:
            current_game = Game.objects.get(game_name=game_id)
        except Game.DoesNotExist:
            return Response({'error': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)
        
        lobby, created = Lobby.objects.get_or_create(game=current_game)
        current_user = request.user
        logger.info(f"User {current_user.username} entering tournament lobby for game {game_id}")

        lobby.users.add(current_user)
        logger.info(f"User {current_user.username} added to tournament lobby {lobby.id}")
        current_user.status = 'waiting'
        current_user.save()

        current_user_stats, created = UserStatsByGame.objects.get_or_create(user=current_user, game=current_game)
        if created:
            logger.info(f"Created new UserStatsByGame for user {current_user.username} and game {current_game.id}")

        potential_opponents = self.find_potential_opponents(current_user_stats, count=3)
        logger.info(f"Potential opponents found: {len(potential_opponents)}")

        if len(potential_opponents) >= 3:
            sorted_opponents = sorted(
                [current_user_stats] + potential_opponents,
                key=lambda stats: Decimal(stats.parties_ratio),
                reverse=True
            )

            # First match: current_user vs opponent with highest ratio
            current_user_match_opponent = sorted_opponents[1].user

            # Second match: remaining two opponents
            match_opponent_1 = sorted_opponents[2].user
            match_opponent_2 = sorted_opponents[3].user

            # Create parties
            party1 = Party.objects.create(
                game=current_game,
                player1=current_user,
                player2=current_user_match_opponent,
                status='waiting'
            )
            party2 = Party.objects.create(
                game=current_game,
                player1=match_opponent_1,
                player2=match_opponent_2,
                status='waiting'
            )

            current_user.status = 'playing'
            current_user_match_opponent.status = 'playing'
            match_opponent_1.status = 'playing'
            match_opponent_2.status = 'playing'

            current_user.save()
            current_user_match_opponent.save()
            match_opponent_1.save()
            match_opponent_2.save()

            opponent_data = CustomUserSerializer(current_user_match_opponent).data
            party1_data = PartySerializer(party1).data
            party2_data = PartySerializer(party2).data

            # Serialize the other two opponents
            match_opponent_1_data = CustomUserSerializer(match_opponent_1).data
            match_opponent_2_data = CustomUserSerializer(match_opponent_2).data

            return Response({
                'status': 'matched',
                'opponent': opponent_data,
                'party1': party1_data,
                'party2': party2_data,
                'game': current_game.id,
                'match_opponent_1': match_opponent_1_data,
                'match_opponent_2': match_opponent_2_data
            }, status=status.HTTP_201_CREATED)
        
        logger.info("Not enough opponents found, user still waiting...")
        return Response({'status': 'waiting'}, status=status.HTTP_200_OK)

    def get_game_name_by_lobby_id(self, lobby_id):
        lobby_game_mapping = {
            '2': 'pong',
            '3': 'memory',
        }
        return lobby_game_mapping.get(lobby_id)
    
    def find_potential_opponents(self, current_user_stats, count=3):
        all_stats = UserStatsByGame.objects.filter(game=current_user_stats.game, user__status='online').exclude(user=current_user_stats.user)

        # Sort potential opponents by closeness to current user's parties_ratio
        sorted_opponents = sorted(
            all_stats,
            key=lambda stats: abs(Decimal(stats.parties_ratio) - Decimal(current_user_stats.parties_ratio))
        )
        logger.info(f"Potential opponents sorted by parties_ratio: {sorted_opponents}")

        return sorted_opponents[:count]
