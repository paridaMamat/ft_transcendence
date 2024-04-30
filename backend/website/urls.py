from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from . import views
from .views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    #path("", views.index, name='index'),
    path('', include(router.urls)),
    path("sections/<int:num>", views.section, name='section'),
]

urlpatterns += router.urls