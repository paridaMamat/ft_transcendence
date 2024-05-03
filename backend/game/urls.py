from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from . import views
from .views import *

router = DefaultRouter()
#router.register(r'game', GameViewSet, basename='game')
#router.register(r'party', PartyViewSet, basename='party')
#router.register(r'tournament', TournamentViewSet, basename='tournament')

urlpatterns = [
    #path("", views.index, name='index'),
    path('', include(router.urls)),
    #path("sections/<int:num>", views.section, name='section'),
]

urlpatterns += router.urls