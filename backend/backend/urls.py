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
from django.conf import settings
from django.conf.urls.static import static
#from website.views import login_view, register_view, game_welcome_view
from website.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    # Serve SPA's main HTML file for all routes
    # Add other Django views as needed
    path('', login_view, name='login_view'),
    path('register_view/', register_view, name='register_view'),
    path('game_welcome/', game_welcome_view, name='game_welcome'),
    path('website/', include("website.urls")), 
]