
from django.db import models
from typing import Any
from .Party import Party
from django.contrib.auth.models import AbstractUser

# tabs for the Pong Game/Memory in general

class Game(models.Model):
    game_id = models.AutoField(primary_key=True)
    game_name = models.CharField(blank=False) # pong or memory
    img = models.ImageField()
    description = models.TextField()
    rules = models.TextField()
    point_to_win = models.IntegerField(default=5)
    nb_parties_played = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.name} game {self.game_id}"

    def getGameData(self):
         return {
            'game_id':self.game_id,
            'name': self.game_name,
            'image':self.img,
            'description':self.description,
            'rules':self.rules,
            'points_to_win':self.points_to_win, 
        }

    def getGameStats(self, Party):   #general metrics: nb of parties played
        parties = 
        return