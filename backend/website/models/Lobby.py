from django.db import models
from typing import Any

##############################################
#                                            #
#             Lobby Classes                  #
#                                            #
##############################################

class Lobby(models.Model):
    game = models.OneToOneField('Game', on_delete=models.CASCADE)
    users = models.ManyToManyField('CustomUser', through='UserInLobby', through_fields=('lobby', 'user'))
    def __str__(self):
        return f"lobby {self.id} for {self.game.game_name}"
    
    def getLobbyUsers(self):
        users_list = self.users.all()
        user = [user.id for user in users_list]
        return user

    def lobby_data(self):
        return {
            'id':self.id,
            'users': self.getLobbyUsers(),
        }
    
class UserInLobby(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    lobby = models.ForeignKey('Lobby', on_delete=models.CASCADE)
    entry_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Player {self.user.id} in lobby {self.lobby.id} since {self.entry_at}" 
    # -> litterally :"1[user] in lobby [n]4 since 2024-05-15 14:30:00"
    
    def getUserLobbyData(self):
        return{
            'id':self.id,
            'user':self.user,
            'lobby':self.lobby,
            'entry_at':self.entry_at,
        }
    