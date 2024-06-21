from django.urls import path, include
from .api import *
from .api.customUser_api import CustomUserViewSet
from .api.lobby_api import LobbyViewSet, UserInLobbyViewSet
from .api.party_api import PartyViewSet
from .api.partyInTour_api import PartyInTournamentViewSet
from .api.game_api import GameViewSet
# from .api.auth42_api import AuthUrlViewSet
from .api.userStats_api import UserStatsViewSet
from .api.tournament_api import TournamentViewSet
#from django.conf import settings
#from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
#from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='users') # to get current user infos, use /users/me
router.register(r'party', PartyViewSet, basename='party')
router.register(r'party_in_tour', PartyInTournamentViewSet, basename='party_in_tour')
router.register(r'lobbies', LobbyViewSet, basename='lobbies')
router.register(r'user_in_lobby', UserInLobbyViewSet, basename='user_in_lobby') # to get current user infos, use /user_in_lobby/me
router.register(r'tournament', TournamentViewSet, basename='tournament')
router.register(r'game', GameViewSet, basename='game')
router.register(r'user_stats', UserStatsViewSet, basename='user_stats') # to get current user infos, use /user_stats/me
# router.register(r'auth42', AuthUrlViewSet, basename='auth42')

urlpatterns = [
	path('', include(router.urls)),
	path('users/update_alias/<int:pk>/', CustomUserViewSet.as_view({'put': 'update_alias'}), name='update_alias'),
    # path('retrieve5first/', UserStatsViewSet.retrieve5first, name='retrieve5first'),
]

urlpatterns += router.urls