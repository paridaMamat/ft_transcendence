from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, CustomUserUpdateForm
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
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

@permission_classes([IsAuthenticated])
@login_required
def account_settings(request):
    if request.method == 'POST':
        user_form = CustomUserUpdateForm(request.POST, request.FILES, instance=request.user)

        if user_form.is_valid():
                user = user_form.save()
                messages.success(request, 'Vos informations ont été mises à jour avec succès!')
                JsonResponse({'success': True, 'redirect_url': ('#account_settings')})
        else:
                messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')

    else:
        user_form = CustomUserUpdateForm(instance=request.user)

    context = {
        'user_form': user_form,
    }
    return render(request, 'account_settings.html', context)



@permission_classes([IsAuthenticated])
@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': form.errors})
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'password_change.html', {'form': form})

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

@permission_classes([IsAuthenticated])
@login_required
def lobby_view(request):
    return render(request, "lobby.html")

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
    return render(request, "createTournament.html")

@permission_classes([IsAuthenticated])
@login_required
def page_finale_view(request):
    return render(request, "page_finale.html")

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

