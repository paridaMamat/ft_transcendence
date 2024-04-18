from django.db import models
from typing import Any
from .UserData import CustomUser
from .Party import PongParty, MemoryParty
from django.contrib.auth.models import AbstractUser

# tabs for 1 party of Pong Game/Memory

class PongStatsUser(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE) #one-to-many relationship
    game_id = models.ForeignKey(PongParty, on_delete=models.CASCADE) #one-to-many relationship
    won_game = models.IntegerField(default=0)
    lost_game = models.IntegerField(default=0)
    shortest_game = models.DurationField(blank=False) # info a recuperer dans 1 autre tab
    longuest_game = models.DurationField(blank=False) # info a recuperer dans 1 autre tab
    ratio = models.IntegerField(default=0)			  # info a calculer	
    highest_score = models.IntegerField(default=0)
    lowest_score = models.IntegerField(default=0)
    level = models.IntegerField(default=0)
    nb_tour_played = models.IntegerField(default=0) # info a calculer
    won_tour = models.IntegerField(default=0)		# info a calculer
    tour_ratio = models.IntegerField(default=0)		# info a calculer
    
    #def update_pong()

    #def user_stat_by_pong_game(self)

class MemoryStatsUser(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE) #one-to-many relationship
    game_id = models.ForeignKey(PongParty, on_delete=models.CASCADE) #one-to-many relationship
    won_game = models.IntegerField(default=0)
    lost_game = models.IntegerField(default=0)
    shortest_game = models.DurationField(blank=False) # info a recuperer dans 1 autre tab
    longuest_game = models.DurationField(blank=False) # info a recuperer dans 1 autre tab
    ratio = models.IntegerField(default=0)			  # info a calculer	
    highest_score = models.IntegerField(default=0)
    lowest_score = models.IntegerField(default=0)
    level = models.IntegerField(default=0)
    nb_tour_played = models.IntegerField(default=0) # info a calculer
    won_tour = models.IntegerField(default=0)		# info a calculer
    tour_ratio = models.IntegerField(default=0)		# info a calculer
    

    #def update_memory()

    #def user_stat_by_memory_game(self)


