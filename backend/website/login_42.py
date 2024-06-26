from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate
from rest_framework.response import Response
from rest_framework import status
from .forms import CustomUserCreationForm, CustomUserUpdateForm
from .models import CustomUser
from rest_framework.permissions import AllowAny
from .serializers import *
from .utils import get_tokens_for_user
from rest_framework.decorators import api_view, permission_classes
import requests
from django.conf import settings
import random
import string
import json

def get_user_data_from_code(code, request):
    token_url = 'https://api.intra.42.fr/oauth/token'
    data = {
        'grant_type': 'authorization_code',
        'client_id': settings.CLIENT_ID,
        'client_secret': settings.CLIENT_SECRET,
        'code': code,
        'redirect_uri': settings.REDIRECT_URI,
    }

    try:
        response = requests.post(token_url, data=data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return HttpResponse(f"Error: Unable to retrieve tokens. Details: {str(e)}", status=500)
    
    tokens = response.json()
    access_token = tokens.get('access_token')
    refresh_token = tokens.get('refresh_token')

    request.session['access_token'] = access_token
    request.session['refresh_token'] = refresh_token

    user_info_url = 'https://api.intra.42.fr/v2/me'
    headers = {'Authorization': f'Bearer {access_token}'}

    try:
        user_info_response = requests.get(user_info_url, headers=headers)
        user_info_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return HttpResponse(f"Error: Unable to retrieve user info. Details: {str(e)}", status=500)
    
    user_info = user_info_response.json()
    avatar_url = user_info.get('image', {}).get('link')  # Get the main avatar link
    
    # Log user info and avatar URL
    print(f"User Info: {user_info}")
    print(f"Avatar URL: {avatar_url}")
    
    return {
        'username': user_info.get('login'),
        'email': user_info.get('email'),
        'first_name': user_info.get('first_name'),
        'last_name': user_info.get('last_name'),
        'avatar_url': avatar_url
    }

@api_view(['GET'])
@permission_classes([AllowAny])
def handle_42_redirect(request):
    code = request.GET.get('code')
    if not code:
        return HttpResponse("Error: No code provided", status=400)
    
    user_data = get_user_data_from_code(code, request)
    if isinstance(user_data, HttpResponse):
        return user_data

    username = user_data.get('username')
    email = user_data.get('email')
    first_name = user_data.get('first_name')
    last_name = user_data.get('last_name')
    avatar_url = user_data.get('avatar_url')

    print(f"Received user data: {user_data}")

    user = CustomUser.objects.filter(username=username).first()
    if not user:
        default_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        
        # Download and save the avatar
        avatar_content = None
        if avatar_url:
            print(f"Downloading avatar from {avatar_url}")
            avatar_content = download_image(avatar_url)
            if not avatar_content:
                print("Failed to download avatar.")
        
        form_data = {
            'username': username,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'password1': default_password,
            'password2': default_password,
        }
        form = CustomUserCreationForm(form_data)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(default_password)
            if avatar_content:
                avatar_filename = get_image_filename(avatar_url, username)
                user.avatar.save(avatar_filename, avatar_content)
            user.save()
        else:
            return Response({'error': form.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        # Update user details and avatar if needed
        form_data = {
            'username': username,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'avatar': user.avatar  # Keep current avatar if not updating
        }
        form = CustomUserUpdateForm(form_data, instance=user)
        
        if avatar_url:
            print(f"Updating avatar for user {username}")
            avatar_content = download_image(avatar_url)
            if avatar_content:
                avatar_filename = get_image_filename(avatar_url, username)
                user.avatar.save(avatar_filename, avatar_content)
            else:
                print("Failed to update avatar.")
        
        if form.is_valid():
            form.save()
        else:
            return Response({'error': form.errors}, status=status.HTTP_400_BAD_REQUEST)

        default_password = None

    if default_password:
        user = authenticate(username=username, password=default_password)
    else:
        # Existing user, attempt to authenticate without password
        user = CustomUser.objects.get(username=username)

    if not user:
        return Response({'error': 'Authentication failed'}, status=status.HTTP_400_BAD_REQUEST)

    login(request, user)
    tokens = get_tokens_for_user(user)
    return render(request, 'auth42.html', {
        'success': True,
        'message': 'Tokens generated successfully.',
        'tokens': json.dumps(tokens)  # Ensure tokens are serialized to JSON
    })


'''@api_view(['GET'])
@permission_classes([AllowAny])
def handle_42_redirect(request):
    code = request.GET.get('code')
    if not code:
        return HttpResponse("Error: No code provided", status=400)
    
    user_data = get_user_data_from_code(code, request)
    if isinstance(user_data, HttpResponse):
        return user_data

    username = user_data.get('username')
    email = user_data.get('email')
    first_name = user_data.get('first_name')
    last_name = user_data.get('last_name')
    avatar_url = user_data.get('avatar_url')

    print(f"Received user data: {user_data}")

    user = CustomUser.objects.filter(username=username).first()
    if not user:
        default_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        form_data = {
            'username': username,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'password1': default_password,
            'password2': default_password,
            'avatar': avatar_url
        }
        form = CustomUserCreationForm(form_data)
        if form.is_valid():
            user = form.save()
            user.set_password(default_password)

            # Download and save the avatar
            if avatar_url:
                print(f"Downloading avatar from {avatar_url}")
                avatar_content = download_image(avatar_url)
                if avatar_content:
                    avatar_filename = get_image_filename(avatar_url, username)
                    user.avatar.save(avatar_filename, avatar_content)
                else:
                    print("Failed to download avatar.")

            user.save()
        else:
            return Response({'error': form.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        default_password = None

    if default_password:
        user = authenticate(username=username, password=default_password)
    else:
        # Existing user, attempt to authenticate without password
        user = CustomUser.objects.get(username=username)

    if not user:
        return Response({'error': 'Authentication failed'}, status=status.HTTP_400_BAD_REQUEST)

    login(request, user)
    tokens = get_tokens_for_user(user)
    return render(request, 'auth42.html', {
        'success': True,
        'message': 'Tokens generated successfully.',
        'tokens': json.dumps(tokens)  # Ensure tokens are serialized to JSON
    })'''