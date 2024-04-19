from django.db import models
from typing import Any
from .UserData import CustomUser
from .Party import PongParty, MemoryParty
from .Games import PongGame, MemoryGame 
from django.contrib.auth.models import AbstractUser

# tabs for the Lobby (playing area), useful to monitore the users' presence

class PongLobby(models.Model):
    id = models.AutoField(primary_key=True)
    game = models.OneToOneField('PongGame', on_delete=models.CASCADE)
    users = models.ManyToManyField('CustomUser', through='UserInPongLobby', through_fields=('lobby', 'user'))
    
    def __str__(self):
        return f"lobby {self.id} for {self.ponggame.name}"

    def update_pong_data(self):
        return

    def method2(self):
        return

    def method3(self):
        return
    
class UserInPongLobby(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    lobby = models.ForeignKey('Lobby', on_delete=models.CASCADE)
    entry_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.id} in lobby {self.lobby.id} since {self.entry_at}
    
    #def update_pong()

    def update_pong_data(won, losse, ratio, duration, level ...):
        return

    def method2(self):
        return

    def method3(self):
        return
    
class MemoryLobby(models.Model):
    mem_id = models.AutoField(primary_key=True)
    game = models.OneToOneField('MemoryGame', on_delete=models.CASCADE)
	users = models.ManyToManyField('CustomUser', through='UserInMemoryLobby', through_fields=('lobby', 'user'))
	
    def __str__(self):
        return
    
    def update_memory_data(self):
        return

    def method2(self):
        return

    def method3(self):
        return


class UserInMemoryLobby(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    lobby = models.ForeignKey('Lobby', on_delete=models.CASCADE)
    entry_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.id}
    
    #def update_pong()

    def update_pong_data(self):
        return