from django.urls import path, include
from .api import *
from .api.customUser_api import CustomUserViewSet
from .api.lobby_api import LobbyViewSet, UserInLobbyViewSet
from .api.party_api import PartyViewSet
from .api.partyInTour_api import PartyInTournamentViewSet
from .api.game_api import GameViewSet
from .api.userStats_api import UserStatsViewSet
from .api.tournament_api import TournamentViewSet
from .views import *
from .views_api import *
from .views import *
from .views_api import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='users') # to get current user infos, use /users/me
router.register(r'party', PartyViewSet, basename='party')
router.register(r'party_in_tour', PartyInTournamentViewSet, basename='party_in_tour')
router.register(r'lobbies', LobbyViewSet, basename='lobbies')
router.register(r'user_in_lobby', UserInLobbyViewSet, basename='user_in_lobby') # to get current user infos, use /user_in_lobby/me
router.register(r'tournament', TournamentViewSet, basename='tournament')
router.register(r'game', GameViewSet, basename='game')
router.register(r'user_stats', UserStatsViewSet, basename='user_stats') # to get current user infos, use /user_stats/me

urlpatterns = [
	path('', include(router.urls)),
    path('party/retrievePartyByGame/<int:game_id>/<int:user_id>/', PartyViewSet.as_view({'get': 'retrievePartyByGame'}), name='retrieve-party-by-game'),
    path('user_stats/retrieveTopFive/<int:game_id>/', UserStatsViewSet.as_view({'get': 'retrieveTopFive'}), name='retrieve-top-five'),
    path('user_stats/retrieveMyBoard/<int:game_id>/', UserStatsViewSet.as_view({'get': 'retrieveMyBoard'}), name='retrieve-my-board'),
    path('users/add_friends/<int:pk>/', CustomUserViewSet.as_view({'post': 'add_friends'}), name='add-friends'),
    path('users/remove_friends/<int:pk>/', CustomUserViewSet.as_view({'post': 'remove_friends'}), name='remove-friends'),
    path('users/retrieve_friends_data/<int:pk>/', CustomUserViewSet.as_view({'get': 'retrieve_friends_data'}), name='retrieve-friends-data'),
]

urlpatterns += router.urls