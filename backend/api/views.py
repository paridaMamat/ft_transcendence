from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from website.forms import CustomUserCreationForm
from .serializers import UserSerializer
from rest_framework import viewsets

class MaVue(APIView):
    def get(self, request):
        formulaire = CustomUserCreationForm()
        return render(request, 'mon_template.html', {'formulaire': formulaire})

    def post(self, request):
        formulaire = CustomUserCreationForm(request.POST)
        if formulaire.is_valid():
            serializer = UserSerializer(data=formulaire.cleaned_data)
            if serializer.is_valid():
                # Faites quelque chose avec les données sérialisées
                return Response(serializer.data)
        return Response(status=400)
