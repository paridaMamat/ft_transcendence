from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from django.conf import settings

class AuthUrlView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        client_id = settings.CLIENT_ID
        redirect_uri = settings.REDIRECT_URI
        scopes = 'public'

        auth_url = (
            f'https://api.intra.42.fr/oauth/authorize?'
            f'client_id={client_id}&redirect_uri={redirect_uri}&'
            f'scope={scopes}&response_type=code'
        )
        return JsonResponse({'authUrl': auth_url})