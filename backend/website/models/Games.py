
from django.db import models
from typing import Any
from .UserData import CustomUser
from django.contrib.auth.models import AbstractUser

# tabs for the Pong Game/Memory in general

class PongGame(models.Model):
    game_id = models.AutoField(primary_key=True)
    name = models.CharField(blank=False)
    start_time = models.DateTimeField ()
    end_time = models.DateTimeField ()
    duration = models.DateTimeField ()
    date = models.DateField(auto_now=1)
    played_parties = models.IntegerField(default=0)
    winner = models.CharField(blank=False, unique=True)
    def __str__(self):
        return f"{self.name} ponggame {self.game_id}"
    
    def update_game_data(played_party):
        return

    def method2(self):
        return

    def method3(self):
        return

class MemoryGame(models.Model):
    game_id = models.AutoField(primary_key=True)
    nb_players = models.IntegerField(default=0)
    start_time = models.DateTimeField ()
    end_time = models.DateTimeField ()
    duration = models.DateTimeField ()
    date = models.DateField(auto_now=1)
    played_parties = models.IntegerField(default=0)
    winner = models.CharField(blank=False, unique=True)
    def __str__(self):
        return f"{self.name} memorygame {self.game_id}"
    
    #def update()

    #def user_stat_by_game(self)

    def method2(self):
        return

    def method2(self):
        return

    def method3(self):
        return
