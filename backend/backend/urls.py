"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static
from website.views import *
from website.login_42 import *
from website.api.auth42_api import AuthUrlView
from website.serializers import *
from django.views.i18n import *
from django.contrib.auth.views import LogoutView, PasswordChangeView
#from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


# urlpatterns = [
#     path('set-language/', set_language, name='set_language'),
#     # path('', redirect_to_default_language),
# ]
urlpatterns =[
    path('admin/', admin.site.urls),
    path('api/', include('website.urls')),

    path('', base, name='base'),
    path('login/', LoginView.as_view(), name='login'),
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('register/', register_view, name='register'),
    path('friends/', friends_view, name='friends'),
    path('profil/', profil_view, name='profile'),
	path('error_404/', error_view, name='error_404'),
	path('about_us/', about_us_view, name='about_us'),
    path('create_tournament/', create_tournament_view, name='contact'),
    path('lobby/', lobby_view, name='lobby'),
    path('lobby_tournoi/', lobby_tournoi_view, name='tournoi_view'),
    path('lobby_partie/', lobby_partie_view, name='partie_view'),
	path('verify_otp/', OTPVerificationView.as_view(), name='verify_otp'),
    path('enable_2fa/', Enable2FAView.as_view(), name='enable_2fa'),
    path('start_AI/', start_AI, name='start_AI'),
    path('handle-42-redirect/', handle_42_redirect, name='handle_42_redirect'),
	path('auth42/', AuthUrlView.as_view(), name='auth42'),
    path('page_finale/', page_finale_view, name='page_finale'),

	
    path('accueil/', accueil, name='accueil'),
    path('games_page/', games_view, name='games_page/'),
	path('AI/', AI_view, name='AI'),
    path('pong3D/', pong3D, name='pong3D'),
    path('memory_game/', memory_game, name='memory_game'),
    path('account_settings/', account_settings, name='account_settings'),
    path('logout/', LogoutView.as_view(), name='logout'),
	path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('test/', test_view, name='password_change_done'),
    path('set_language/', set_language, name='set_language'),
]
