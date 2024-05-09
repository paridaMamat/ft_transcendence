#from django.shortcuts import render
#from rest_framework.response import Response
#from website.forms import CustomUserCreationForm
#from .serializers import UserSerializer
#from rest_framework import viewsets
#from django import requests
#from website.models import CustomUser
#from game.models import Party, Game, Tournament, Lobby

#class UserViewSet(viewsets.ModelViewSet):
#    def get(self, request):
#        formulaire = CustomUserCreationForm()
#        return render(request, 'mon_template.html', {'formulaire': formulaire})

#    def post(self, request):
#        formulaire = CustomUserCreationForm(request.POST)
#        if formulaire.is_valid():
#            serializer = UserSerializer(data=formulaire.cleaned_data)
#            if serializer.is_valid():
#                # Faites quelque chose avec les données sérialisées
#                return Response(serializer.data)
#        return Response(status=400)

#class UserViewSet(viewsets.ModelViewSet):
#    queryset = CustomUser.objects.all()
#    serializer_class = CustomUser

