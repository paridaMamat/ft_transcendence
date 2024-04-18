from django.db import models
from typing import Any
from .UserData import CustomUser
from django.contrib.auth.models import AbstractUser

# tabs for 1 tournament of Pong Game/Memory

class PongTournament(models.Model):
    tour_id = models.AutoField(primary_key=True)
    tour_name = models.CharField(blank=False, unique=True)
    tour_creator = models.ForeignKey(CustomUser, blank=False)
    nb_rounds = models.IntegerField(blank=False)
    current_round = models.IntegerField()
    nb_players = models.IntegerField(default=0)
    start_time = models.DateTimeField ()
    end_time = models.DateTimeField ()
    duration = models.DateTimeField ()
    date = models.DateField(auto_now=1)
    tour_users = models.ManyToManyField(CustomUser)
    winner = models.ForeignKey(CustomUser)

    def method1(self):
        return

    def method2(self):
        return

    def method3(self):
        return


####################################################

class MemoryTournament(models.Model):
    tour_id = models.AutoField(primary_key=True)
    tour_name = models.CharField(blank=False, unique=True)
    tour_creator = models.ForeignKey(CustomUser, blank=False)
    nb_rounds = models.IntegerField(blank=False)
    current_round = models.IntegerField()
    nb_players = models.IntegerField(default=0)
    start_time = models.DateTimeField ()
    end_time = models.DateTimeField ()
    duration = models.DateTimeField ()
    date = models.DateField(auto_now=1)
    tour_users = models.ManyToManyField(CustomUser)
    winner = models.ForeignKey(CustomUser)

    def method1(self):
        return

    def method1(self):
        return

    def method1(self):
        return

