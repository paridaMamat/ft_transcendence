from django.urls import path
from . import views

urlpatterns = [
    path('', views.TournamentListCreateView.as_view(), name='tournament-list'),
    path('create_tournament/', views.create_tournament, name='create-tournament'),
	path('create_local_tournament/', views.create_local_tournament, name='create-local-tournament'),
	path('<int:tournamentid>/', views.get_tournament_details, name='get_tournament_details'),
	path('<int:tournament_id>/play-next-match', views.play_next_match, name='play-next-match'),
]
