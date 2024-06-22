# from django.contrib.auth import login, authenticate
# from django.contrib.auth.views import LoginView
# from forms import CustomUserCreationForm , CustomUserUpdateForm
# from django.shortcuts import render, get_object_or_404
# from django.http import JsonResponse,  HttpResponse, Http404
# from django.contrib.auth.decorators import login_required
# from utils import verify_otp, get_tokens_for_user
# from django.utils.decorators import method_decorator
# from django.contrib.auth import get_user_model
# from django.utils import translation
# from django.utils.translation import gettext_lazy as _
# import pyotp, qrcode, base64, logging, requests, json, random, string
# from io import BytesIO
# from models import *
# from serializers import *
# from .api import *
# from decimal import Decimal
# from django.conf import settings
# from rest_framework.views import APIView
# from rest_framework import status
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from django.contrib.auth import update_session_auth_hash
# from django.contrib.auth.forms import PasswordChangeForm
# from django.contrib import messages
# from django.views.decorators.http import require_POST

# ######################################################################
# #                                                                    #
# #                         Authentification                           #
# #                                                                    #
# ######################################################################

# class LoginView(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request):
#         return render(request, 'login.html')

#     def post(self, request):
#         serializer = LoginSerializer(data=request.data, context={'request': request})
#         if serializer.is_valid():
#             user = serializer.validated_data.get('user')
#             if (user.status == 'offline'):
#                 user.status = 'online'
#             login(request, user)

#             if user.two_factor_enabled:
#                 # Redirect to OTP verification page
#                 request.session['temp_user_id'] = user.id
#                 return Response({'redirect': True, 'url': '#verify_otp'}, status=status.HTTP_200_OK)
#             else:
#                 # Generate JWT tokens if authentication successful
#                 tokens = get_tokens_for_user(user)
#                 return Response(tokens, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class OTPVerificationView(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request):
#         # Serve the OTP verification page
#         return render(request, 'verify_otp.html')

#     def post(self, request):
#         otp = request.data.get('otp')
#         user_id = request.session.get('temp_user_id')
        
#         if not user_id:
#             return Response({'error': 'Session expired, please login again.'}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             user = CustomUser.objects.get(id=user_id)
#         except CustomUser.DoesNotExist:
#             return Response({'error': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)

#         totp = pyotp.TOTP(user.two_factor_secret)
#         if totp.verify(otp):
#             # OTP is valid, clear the temporary user session
#             del request.session['temp_user_id']
#             # Generate JWT tokens
#             tokens = get_tokens_for_user(user)
#             return Response(tokens, status=status.HTTP_200_OK) # revoir la redir
#         else:
#             return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

# @method_decorator(login_required, name='dispatch')
# class Enable2FAView(APIView):
#     def get(self, request):
#         user = request.user
#         otp_secret = pyotp.random_base32()
#         user.two_factor_secret = otp_secret
#         user.two_factor_enabled = True
#         user.save()

#         # Generate QR code
#         otp_auth_url = pyotp.totp.TOTP(otp_secret).provisioning_uri(name=user.username, issuer_name="ft_transcendence")
#         qr = qrcode.make(otp_auth_url)
#         buffer = BytesIO()
#         qr.save(buffer, format="PNG")
#         qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()

#         # Set temp_user_id in the session
#         request.session['temp_user_id'] = user.id

#         return render(request, 'enable_2fa.html', {'qr_code_base64': qr_code_base64, 'otp_secret': otp_secret})
    
# class ProtectedView(APIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]
    
#     def get(self, request):
#         user = request.user
#         return JsonResponse({'message': 'You are authenticated'})

# def get_user_data_from_code(code, request):
#     token_url = 'https://api.intra.42.fr/oauth/token'
#     data = {
#         'grant_type': 'authorization_code',
#         'client_id': settings.CLIENT_ID,
#         'client_secret': settings.CLIENT_SECRET,
#         'code': code,
#         'redirect_uri': settings.API_42_REDIRECT_URI,
#     }

#     try:
#         response = requests.post(token_url, data=data)
#         response.raise_for_status()
#     except requests.exceptions.RequestException as e:
#         return HttpResponse(f"Error: Unable to retrieve tokens. Details: {str(e)}", status=500)
    
#     tokens = response.json()
#     access_token = tokens.get('access_token')
#     refresh_token = tokens.get('refresh_token')

#     request.session['access_token'] = access_token
#     request.session['refresh_token'] = refresh_token

#     user_info_url = 'https://api.intra.42.fr/v2/me'
#     headers = {'Authorization': f'Bearer {access_token}'}

#     try:
#         user_info_response = requests.get(user_info_url, headers=headers)
#         user_info_response.raise_for_status()
#     except requests.exceptions.RequestException as e:
#         return HttpResponse(f"Error: Unable to retrieve user info. Details: {str(e)}", status=500)
    
#     user_info = user_info_response.json()
#     return {
#         'username': user_info.get('login'),
#         'email': user_info.get('email'),
#         'first_name': user_info.get('first_name'),
#         'last_name': user_info.get('last_name')
#     }

# @api_view(['GET'])
# @permission_classes([AllowAny])
# def handle_42_redirect(request):
#     code = request.GET.get('code')
#     if not code:
#         return HttpResponse("Error: No code provided", status=400)
    
#     user_data = get_user_data_from_code(code, request)
#     if isinstance(user_data, HttpResponse):
#         return user_data

#     username = user_data.get('username')
#     email = user_data.get('email')
#     first_name = user_data.get('first_name')
#     last_name = user_data.get('last_name')

#     user = CustomUser.objects.filter(username=username).first()
#     if not user:
#         default_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
#         form_data = {
#             'username': username,
#             'email': email,
#             'first_name': first_name,
#             'last_name': last_name,
#             'password1': default_password,
#             'password2': default_password,
#         }
#         form = CustomUserCreationForm(form_data)
#         if form.is_valid():
#             user = form.save()
#             user.set_password(default_password)
#             user.save()
#         else:
#             return Response({'error': form.errors}, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         default_password = None

#     if default_password:
#         user = authenticate(username=username, password=default_password)
#     else:
#         # Existing user, attempt to authenticate without password
#         user = CustomUser.objects.get(username=username)

#     if not user:
#         return Response({'error': 'Authentication failed'}, status=status.HTTP_400_BAD_REQUEST)

#     login(request, user)
#     tokens = get_tokens_for_user(user)
#     return render(request, 'auth42.html', {
#         'success': True,
#         'message': 'Tokens generated successfully.',
#         'tokens': json.dumps(tokens)  # Ensure tokens are serialized to JSON
#     })

# ######################################################################
# #                                                                    #
# #                         Friends                                    #
# #                                                                    #
# ######################################################################

# User = get_user_model()

# @method_decorator(login_required, name='dispatch')
# class AddFriendView(APIView):
#     permission_classes = [IsAuthenticated]

#     def add_friend(self, request):
#         serializer = CustomUserSerializer(data=request.data, context={'request': request})
#         new_friend_username = request.data.get('username')

#         if new_friend_username:
#             try:
#                 new_friend = CustomUser.objects.get(username=new_friend_username)
#                 user = request.user
#                 if new_friend in user.friends.all():
#                     return Response({'error': 'User is already a friend.'}, status=status.HTTP_400_BAD_REQUEST)

#                 user.friends.add(new_friend)
#                 user.save()
#                 return Response({'success': True, 'redirect': True, 'url': '#friends'}, status=status.HTTP_201_CREATED)
#             except CustomUser.DoesNotExist:
#                 return Response({'error': 'User with username not found.'}, status=status.HTTP_404_NOT_FOUND)
#         else:
#             return Response({'error': 'Missing friend username in request data.'}, status=status.HTTP_400_BAD_REQUEST)
        
#     def delete(self, request):  # Delete a friend
#         friend_username = request.data.get('friend')
#         friend = get_object_or_404(User, username=friend_username)
#         user = request.user
#         user.friends.remove(friend)
#         user.save()
#         return Response({'redirect': True, 'url': '#friends'}, status=status.HTTP_200_OK)

# ######################################################################
# #                                                                    #
# #                         Lobbby / Matchmaking                       #
# #                                                                    #
# ######################################################################

# # Définissez le logger pour ce module
# logger = logging.getLogger(__name__)

# class LobbyView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         lobby_id = request.GET.get('id')
#         logger.info("get lobby view")
#         return render(request, 'lobby.html', {'id': lobby_id})

#     def post(self, request):
#         logger.info("post lobby view")
#         lobby_id = request.data.get('id')

#         game_id = self.get_game_name_by_lobby_id(lobby_id)
#         if not game_id:
#             logger.error(f"Invalid lobby ID: {lobby_id}")
#             return Response({'error': 'Invalid lobby ID'}, status=status.HTTP_400_BAD_REQUEST)
        
#         return self.handle_lobby_request(request, game_id)
        
#     def handle_lobby_request(self, request, game_id):

#         try:
#             current_game = Game.objects.get(game_name=game_id)
#         except Game.DoesNotExist:
#             return Response({'error': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)
        
#         lobby, created = Lobby.objects.get_or_create(game=current_game)
#         current_user = request.user
#         logger.info(f"User {current_user.username} entering lobby for game {game_id} / current_game {current_game.id}")

#         lobby.users.add(current_user)
#         logger.info(f"User {current_user.username} added to lobby {lobby.id}")
#         current_user.status = 'waiting'
#         current_user.save()

#         current_user_stats, created = UserStatsByGame.objects.get_or_create(user=current_user, game=current_game)
#         if created:
#             logger.info(f"Created new UserStatsByGame for user {current_user.username} and game {current_game.id}")

#         potential_opponents = self.find_potential_opponents(current_user_stats)
#         logger.info(f"Potential opponents found: {len(potential_opponents)}")

#         if potential_opponents:
#             opponent_stats = potential_opponents[0]
#             opponent = opponent_stats.user
#             logger.info(f"Match found: {opponent.username} with a parties_ratio of {opponent_stats.parties_ratio}")

#             lobby.users.add(opponent)

#             party = Party.objects.create(
#                 game=current_game,
#                 player1=current_user,
#                 player2=opponent,
#                 status='waiting'
#             )

#             current_user.status = 'waiting'
#             opponent.status = 'waiting'
#             current_user.save()
#             opponent.save()

#             lobby.users.remove(current_user)
#             lobby.users.remove(opponent)

#             opponent_data = CustomUserSerializer(opponent).data
#             party_data = PartySerializer(party).data

#             return Response({
#                 'status': 'matched',
#                 'opponent': opponent_data,
#                 'party': party_data,
#                 'game': current_game.id
#             }, status=status.HTTP_201_CREATED)
        
#         logger.info("No match found, user still waiting...")
#         return Response({'status': 'waiting'}, status=status.HTTP_200_OK)

#     def get_game_name_by_lobby_id(self, lobby_id):
#         lobby_game_mapping = {
#             '2': 'pong',
#             '3': 'memory',
#         }
#         return lobby_game_mapping.get(lobby_id)
    
#     def find_potential_opponents(self, current_user_stats):
#         all_stats = UserStatsByGame.objects.filter(game=current_user_stats.game, user__status='online').exclude(user=current_user_stats.user)

#         # Sort potential opponents by closeness to current user's parties_ratio
#         sorted_opponents = sorted(
#             all_stats,
#             key=lambda stats: abs(Decimal(stats.parties_ratio) - Decimal(current_user_stats.parties_ratio))
#         )
#         logger.info(f"Potential opponents sorted by parties_ratio: {sorted_opponents}")

#         return sorted_opponents
