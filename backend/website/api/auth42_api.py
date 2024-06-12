from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from django.conf import settings

class AuthUrlView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        redirect_uri = settings.API_42_REDIRECT_URI
        scopes = 'public'

        auth_url = f'https://api.intra.42.fr/oauth/authorize?client_id={settings.CLIENT_ID}&redirect_uri={redirect_uri}&scope={scopes}&response_type=code'
        return JsonResponse({'authUrl': auth_url})
