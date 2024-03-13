from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register),
    path('login', views.login),
    path('verify_token', views.verify_token),
    path('get_user_from_token', views.get_user_from_token),
    path('update_user', views.update_user),
    path('get_users', views.get_users),
    path('get_user/<str:username>/', views.get_user_from_username),
	path('logout', views.logout),
]