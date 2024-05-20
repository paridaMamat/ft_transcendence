from django.contrib import admin
from .models import *

# Register your models here.
# pour qu'un modèle soit visible et administrable dans l'interface d'administration,
# vous devez l'enregistrer dans le fichier admin.py de votre application
from django.contrib.auth.admin import UserAdmin
#En utilisant UserAdmin, vous appliquez les paramètres par défaut
#et les fonctionnalités spécifiques à l'administration des utilisateurs de Django à votre modèle CustomUser.

admin.site.register(Game)
admin.site.register(PartyInTournament)
admin.site.register(Lobby)
admin.site.register(Party)
admin.site.register(UserInLobby)
admin.site.register(Tournament)