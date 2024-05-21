from django.urls import path, include
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('users_list/', CustomUserViewSet.as_view({'get':'list'}), name='users_list'),
	path('user_detail/<int:id>/', views.user_detail, name='user_detail'),
	path('user_info/', views.user_info, name='user_info'),

	#path('games_list/', GameViewSet.as_view({'get':'list'}), name='games_list'),
	##path('games_list/', views.games_list, name='games_list'),
	#path('game_detail/<int:id>/', views.game_detail, name='game_detail'),
	#path('game_info/', views.game_info, name='game_info'),
	
    #path('parties_list/', PartyViewSet.as_view({'get':'list'}), name='parties_list'),
	##path('parties_list/', views.parties_list, name='parties_list'),
	#path('party_detail/<int:id>/', views.party_detail, name='party_detail'),
	#path('party_info/', views.party_info, name='party_info'),
	
    ##path('parties_tour_list/', PartyInTournamentViewSet.as_view({'get':'list'}), name='partiesStats_list'),
	#path('parties_stats_list/', views.parties_stats_list, name='partiesStats_list'),
	#path('party_stats_detail/<int:id>/', views.party_stats_detail, name='party_stats_detail'),
	#path('party_tour_info/', views.party_stats_info, name='party_stats_info'),
	
    #path('lobbies_list/', LobbyViewSet.as_view({'get':'list'}), name='lobbys_list'),
	##path('lobbies_list/', views.lobbies_list, name='lobbies_list'),
	#path('lobby_detail/<int:id>/', views.lobby_detail, name='lobby_detail'),
	#path('lobby_info/', views.lobby_info, name='lobby_info'),
	
    #path('user_in_lobbies_list/', UserInLobbyViewSet.as_view({'get':'list'}), name='user_in_lobby_list'),
	##path('user_in_lobbies_list/', views.user_in_lobbies_list, name='user_in_lobbies_list'),
	#path('user_in_lobby_detail/<int:id>/', views.user_in_lobby_detail, name='user_in_lobby_detail'),
	#path('user_in_lobby_info/', views.user_in_lobby_info, name='user_in_lobby_info'),
	
    #path('tournaments_list/', TournamentViewSet.as_view({'get':'list'}), name='tournaments_list'),
	##path('tournaments_list/', views.tournaments_list, name='tournaments_list'),
	#path('tournament_detail/<int:id>/', views.tournament_detail, name='tournament_detail'),
	#path('tournament_info/', views.tournament_info, name='tournament_info'),
]