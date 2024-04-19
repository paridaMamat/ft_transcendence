
from django.db import models
from typing import Any
from .UserData import CustomUser
from django.contrib.auth.models import AbstractUser

# tabs for 1 party of Pong Game/Memory

class Party(models.Model):
    game_id = models.AutoField(primary_key=True)
    players = models.ManyToManyField(CustomUser)
    #player2 = models.ManyToManyField(CustomUser, db_table='User/Game junction tab')
    start_time = models.DateTimeField ()
    end_time = models.DateTimeField ()
    duration = models.DateTimeField ()
    date = models.DateField(auto_now=1)
    winner = models.CharField(length=25, unique=True, blank=False)

    def getPartyStats(self):
        return {
            'game_id':self.user_id,
            'players': self.getPlayers(),
            'duration':self.duration,
            'date':self.date,
            'winner':self.winner,
        }

    def getPlayers(self):
        players_list = self.players.all()
        return players_list

    def method3(self):
        return

class PartyStats(models.Model):
    party_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE) #one-to-many relationship
    game_id = models.ForeignKey(Party, on_delete=models.CASCADE) #one-to-many relationship
    won_set = models.IntegerField(default=0)
    lost_set = models.IntegerField(default=0)
    ratio = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    winner = models.BooleanField(default=False, blank=False)
    def __str__(self):
        return f"{self.party_id} party {self.game_id}"

    def getPartyStats(self):
         return {
            'party_id':self.party_id,
            'user_id': self.user_id,
            'won_set':self.won_set,
            'lost_set':self.lost_set,
            'ratio':self.getRatio(),
            'score':self.score,
            'winner':self.winner,
        }
    
    def getRatio(self):
        self.ratio = self.won_set / self.lost_set * 100
        return self.ratio