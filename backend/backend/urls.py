"""
URL configuration for backend project.

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

#include is used to include the urls from the website app

from django.contrib import admin
from django.urls import path
#from website.views import home
from website.views import user_first_page, login_view, user_registration_page, already_registered


urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', home, name='home'),
    path('', user_first_page, name='user_first_page'),
    path('login/', login_view, name='login'),
    path('inscription/', user_registration_page, name='inscription'),
    path('already_registered/', already_registered, name='already_registered'),

]
