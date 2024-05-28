from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse,  HttpResponse, Http404
from .models import CustomUser
from .serializers import *
from .viewsets import *
import requests
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from .utils import verify_otp, get_tokens_for_user
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated

#####################################
#                                   #
#           Django Views            #
#                                   #
#####################################

class LoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            login(request, user)
            # Generate JWT tokens if authentication successful
            tokens = get_tokens_for_user(user)
            return Response(tokens, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request):
        user = request.user
        print("In my protected views my user is : ", user)
        return JsonResponse({'message': 'You are authenticated'})

def logout_view(request):
    logout(request)
    return redirect('login_view')

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
            user = form.save()  # This line assigns the user instance to the 'user' variable
            login(request, user)  # Now 'user' is defined and can be used here
            #redirect_url = reverse('login',args=['login'])
            #return redirect('login')
            return render(request, 'login.html')
        else:
            return JsonResponse({'error': form.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def friends_view(request):
    print("In my firends_views my user is : ", request.user)  # Debugging: Print the current user
    return render(request, 'friends.html')

@permission_classes([IsAuthenticated])
@login_required
def accueil(request):
    return render(request, "accueil.html")

@login_required
def account_settings(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        # Valider les données du formulaire ici

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

def index(request):
    return render(request, "index.html")
    
def connection(request):
    return render(request, "connection.html")

def games_view(request):
    return render(request, "games.html")

def AI_view(request):
    return render(request, "AI.html")

def pong3D(request):
    return render(request, "pong3D.html")

def memory_game(request):
    return render(request, "memory_game.html")


#@api_view(['GET','POST'])
#@login_required
#def users_list(request):
#    if request.method == 'POST':
#        serializer = CustomUserSerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
#    elif request.method == 'GET':
#        users = CustomUser.objects.all()
#        serializer = CustomUserSerializer(users, many=True)
#        return JsonResponse(serializer.data, safe=False)
#    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#@api_view(['GET'])
#@login_required
#def user_info(request):
#    user = request.user
#    serializer = CustomUserSerializer(user)
#    return JsonResponse(serializer.data, safe=False)
    
#@api_view(['GET', 'PUT', 'DELETE'])
#@login_required
#def user_detail(request, id):
#    try:
#        user = CustomUser.objects.get(pk=id)
#    except CustomUser.DoesNotExist:
#        return JsonResponse(status=status.HTTP_404_NOT_FOUND)

#    if request.method == 'GET':
#        serializer = CustomUserSerializer(user)
#        return JsonResponse(serializer.data)

#    elif request.method == 'PUT':
#        serializer = CustomUserSerializer(user, data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return JsonResponse(serializer.data)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#    elif request.method == 'DELETE':
#        user.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)