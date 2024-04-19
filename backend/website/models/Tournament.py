from django.db import models
from typing import Any
from .UserData import CustomUser
from django.contrib.auth.models import AbstractUser

# tabs for general data of 1 tournament of Pong Game/Memory

class Tournament(models.Model):
    tour_id = models.AutoField(primary_key=True)
    tour_name = models.CharField(blank=False, unique=True)
    tour_game = models.CharField(blank=False) #pong or memory
    tour_creator = models.ForeignKey(CustomUser, blank=False)
    creation_date = models.DateField(auto_now=1)
    nb_rounds = models.IntegerField(default=5, blank=False)
    current_round = models.IntegerField()
    nb_players = models.IntegerField(default=0)
    start_time = models.DateTimeField ()
    end_time = models.DateTimeField ()
    duration = models.DateTimeField ()
    tour_users = models.ManyToManyField(CustomUser)
    winner = models.ForeignKey(CustomUser)
    def __str__(self):
        return f"{self.tour_name} tournament {self.tour_id}"
    
    def getTourPlayers(self):
        return

    def getRank(self):  # tab resuming the final ranking
        return

    def getTourStats(self):
        return

