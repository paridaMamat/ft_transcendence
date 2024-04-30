
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.http import JsonResponse,  HttpResponse, Http404
from .models import CustomUser
from .serializers import UserSerializer, FullUserSerializer
from rest_framework.views import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
import requests

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        form = AuthenticationForm(request, data=request.data)
        if form.is_valid():
            # Créez un nouvel objet CustomUser en utilisant les données du formulaire
            user = form.save()
            # Sérialisez le nouvel objet CustomUser
            serializer = UserSerializer(user)
            # Retournez la réponse avec les données sérialisées et le code de statut 201 Created
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Retournez une réponse avec les erreurs de validation du formulaire et le code de statut 400 Bad Request
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

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
                return JsonResponse({'error': 'Username or password is incorrect.'}, status=400) # Send an error response
        else:
            return JsonResponse({'error': 'Form is invalid.', 'form_errors': form.errors}, status=400)
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() # This line assigns the user instance to the 'user' variable
            login(request, user) # Now 'user' is defined and can be used here
            return JsonResponse({'success': True, 'redirect_url': reverse('login_view')})
        else:
            return JsonResponse({'error': form.errors}, status=400)
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def game_welcome_view(request):
    print(request.user) # Debugging: Print the current user
    return render(request, 'game_welcome.html')

def account_settings(request):
    # Récupérer l'utilisateur connecté
    user = request.user
    context = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,

    }
    return render(request, 'account_settings.html', context)

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