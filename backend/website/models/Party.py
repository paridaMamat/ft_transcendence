
from django.db import models
from typing import Any
from .UserData import CustomUser
from django.contrib.auth.models import AbstractUser

# tabs for 1 party of Pong Game/Memory

class PongParty(models.Model):
    game_id = models.AutoField(primary_key=True)
    players = models.ManyToManyField(CustomUser)
    #player2 = models.ManyToManyField(CustomUser, db_table='User/Game junction tab')
    start_time = models.DateTimeField ()
    end_time = models.DateTimeField ()
    duration = models.DateTimeField ()
    date = models.DateField(auto_now=1)
    winner = models.CharField(length=25, unique=True, blank=False)

    def method1(self):
        return

    def method2(self):
        return

    def method3(self):
        return

class PongStats(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE) #one-to-many relationship
    game_id = models.ForeignKey(PongParty, on_delete=models.CASCADE) #one-to-many relationship
    won_set = models.IntegerField(default=0)
    lost_set = models.IntegerField(default=0)
    ratio = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    level = models.IntegerField(default=0)
    winner = models.BooleanField(default=False, blank=False)

    #def update_pong()

    #def user_stat_by_pong_game(self)

    def method1(self):
        return

    def method2(self):
        return

    def method3(self):
        return

class MemoryParty(models.Model):
    game_id = models.AutoField(primary_key=True)
    players = models.ManyToManyField(CustomUser)
    #player2 = models.ManyToManyField(CustomUser, db_table='User/Game junction tab')
    start_time = models.DateTimeField ()
    end_time = models.DateTimeField ()
    duration = models.DateTimeField ()
    date = models.DateField(auto_now=1)
    winner = models.CharField(length=25, unique=True, blank=False)

    def method1(self):
        return

    def method2(self):
        return

    def method3(self):
        return
    
class MemoryStats(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE) #one-to-many relationship
    game_id = models.ForeignKey(PongParty, on_delete=models.CASCADE) #one-to-many relationship
    pairs_set = models.IntegerField(default=0)
    total_flipped_cards = models.IntegerField(default=0)
    ratio = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    winner = models.BooleanField(default=False, blank=False)

    #def update_memory()

    #def user_stat_by_memory_game(self)

    def method1(self):
        return

    def method2(self):
        return

    def method3(self):
        return
