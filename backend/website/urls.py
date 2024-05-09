from django.urls import path, include
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('users_list/', CustomUserViewSet.as_view({'get':'list'}), name='users_list'),
	path('user_detail/<int:id>/', views.user_detail, name='user_detail'),
	path('user_info/', views.user_info, name='user_info'),
  path('accueil/', views.accueil, name='accueil'),
]