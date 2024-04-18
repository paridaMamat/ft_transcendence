
from django.db import models
from typing import Any
from .UserData import CustomUser
from django.contrib.auth.models import AbstractUser

# tabs for the Pong Game/Memory in general

class PongGame(models.Model):
    game_id = models.AutoField(primary_key=True)
    nb_players = models.IntegerField(default=0)
    start_time = models.DateTimeField ()
    end_time = models.DateTimeField ()
    duration = models.DateTimeField ()
    date = models.DateField(auto_now=1)
    played_parties = models.IntegerField(default=0)

    """
    add the functions to get the stats/data here!!

    def [...]
    """

class MemoryGame(models.Model):
    game_id = models.AutoField(primary_key=True)
    nb_players = models.IntegerField(default=0)
    start_time = models.DateTimeField ()
    end_time = models.DateTimeField ()
    duration = models.DateTimeField ()
    date = models.DateField(auto_now=1)
    played_parties = models.IntegerField(default=0)

    #def update()

    #def user_stat_by_game(self)

    """
    add the functions to get the stats/data here!!

    def [...]
    """

#	PARAM DE MODELS
#		primary_key
#		unique
#		default
#		null
#		blank
#		on_delete
	
#	ATTRIBUTS DE MODELS
#		CharField
#		IntegerField
#		DateField
#		FloatField
#		EmailField
#		BooleanField
