
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.http import JsonResponse,  HttpResponse, Http404
from .models import CustomUser
from .serializers import *
import requests
from rest_framework import viewsets, status, generics
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.contrib.auth.decorators import login_required

#---------------------------------------------
# Django REST Framework ViewSets
#---------------------------------------------

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser
   
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = FullUserSerializer
    permission_classes = {IsSuperUser}

@api_view(['POST'])
@login_required
def users_list(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@login_required
def user_info(request):
    user = request.user
    serializer = UserRegistrationSerializer(user)
    return JsonResponse(serializer.data, safe=False)
    
@api_view(['GET', 'PUT', 'DELETE'])
@login_required
def user_detail(request, id):
    try:
        user = CustomUser.objects.get(pk=id)
    except CustomUser.DoesNotExist:
        return JsonResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserRegistrationSerializer(user)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        serializer = UserRegistrationSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# [GET]
#class UserInfo(generics.ListCreateAPIView): 
#    serializer_class = UserRegistrationSerializer

#    def get_queryset(self):
#        queryset = CustomUser.objects.all()
#        username = self.request.query_params.get('username')
#        first_name = self.request.query_params.get('first_name')
#        last_name = self.request.query_params.get('last_name')
#        email = self.request.query_params.get('email')
        
#        if username:
#            queryset = queryset.filter(username=username)
#        if first_name:
#            queryset = queryset.filter(first_name=first_name)
#        if last_name:
#            queryset = queryset.filter(last_name=last_name)
#        if email:
#            queryset = queryset.filter(email=email)
#        if username is None:
#            return Response(queryset.errors, status=status.HTTP_400_BAD_REQUEST)
#        return queryset

## [POST, PUT, DELETE]
#class UserDetail(generics.RetrieveUpdateDestroyAPIView):
#    serializer_class = UserRegistrationSerializer

#    def get_queryset(self):
#         queryset = CustomUser.objects.get(id)
#         user = self.request.query_params.get('username', 'first_name', 'last_name', 'email')
#         if user is None:
#             return Response(queryset.errors, status=status.HTTP_400_BAD_REQUEST)
#         return queryset
    
#---------------------------------------------
# Django Views
#---------------------------------------------

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
        
        # Valider les données du formulaire ici
            user = form.save() # Access the currently logged-in user

        # Mettre à jour les informations de l'utilisateur
            #user.username = username
            #user.first_name = first_name
            #user.last_name = last_name
            #user.email = email
            #user.password1 = pwd
            #user.save()
            serializer = UserRegistrationSerializer(user)  # Sérialiser l'utilisateur nouvellement enregistré
            #return render({'success': True, 'user': serializer.data, 'redirect_url': reverse('login')})
        else:
            return JsonResponse({'error': form.errors}, status=400)
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def welcome_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    print(request.user) # Debugging: Print the current user
    return render(request, 'welcome.html')

def index(request):
    return render(request, "singlepage/index.html")

texts = ["Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam tortor mauris, maximus semper volutpat vitae, varius placerat dui. Nunc consequat dictum est, at vestibulum est hendrerit at. Mauris suscipit neque ultrices nisl interdum accumsan. Sed euismod, ligula eget tristique semper, lecleo mi nec orci. Curabitur hendrerit, est in ",
        "Praesent euismod auctor quam, id congue tellus malesuada vitae. Ut sed lacinia quam. Sed vitae mattis metus, vel gravida ante. Praesent tincidunt nulla non sapien tincidunt, vitae semper diam faucibus. Nulla venenatis tincidunt efficitur. Integer justo nunc, egestas eget dignissim dignissim,  facilisis, dictum nunc ut, tincidunt diam.",
        "Morbi imperdiet nunc ac quam hendrerit faucibus. Morbi viverra justo est, ut bibendum lacus vehicula at. Fusce eget risus arcu. Quisque dictum porttitor nisl, eget condimentum leo mollis sed. Proin justo nisl, lacinia id erat in, suscipit ultrices nisi. Suspendisse placerat nulla at volutpat ultricies"]

def section(request, num):
    if 1 <= num <= 3:
        return HttpResponse(texts[num-1])
    else:
        raise Http404("No such section")

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
        return redirect('game_welcome')

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

texts = ["Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam tortor mauris, maximus semper volutpat vitae, varius placerat dui. Nunc consequat dictum est, at vestibulum est hendrerit at. Mauris suscipit neque ultrices nisl interdum accumsan. Sed euismod, ligula eget tristique semper, lecleo mi nec orci. Curabitur hendrerit, est in ",
        "Praesent euismod auctor quam, id congue tellus malesuada vitae. Ut sed lacinia quam. Sed vitae mattis metus, vel gravida ante. Praesent tincidunt nulla non sapien tincidunt, vitae semper diam faucibus. Nulla venenatis tincidunt efficitur. Integer justo nunc, egestas eget dignissim dignissim,  facilisis, dictum nunc ut, tincidunt diam.",
        "Morbi imperdiet nunc ac quam hendrerit faucibus. Morbi viverra justo est, ut bibendum lacus vehicula at. Fusce eget risus arcu. Quisque dictum porttitor nisl, eget condimentum leo mollis sed. Proin justo nisl, lacinia id erat in, suscipit ultrices nisi. Suspendisse placerat nulla at volutpat ultricies"]

def section(request, num):
    if 1 <= num <= 3:
        return HttpResponse(texts[num-1])
    else:
        raise Http404("No such section")
    
def connection(request):
    return render(request, "connection.html")

def games_view(request):
    return render(request, "games.html")

def AI_view(request):
    return render(request, "AI.html")

def AI_test(request):
    return render(request, "AI_test.html")

def accueil(request):
    return render(request, "accueil.html")

def memory_game(request):
    return render(request, "memory_game.html")
