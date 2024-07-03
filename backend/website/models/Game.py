from django.db import models
from typing import Any

#############################################
#                                           #
#             Game Classes                  #
#                                           #
#############################################

class Game(models.Model):
    game_name = models.CharField(blank=False) # pong or memory
    points_to_win = models.IntegerField(default=5)
    def __str__(self):
        return f"{self.game_name}"

    def getGameData(self):
         return {
            'game_id':self.id,
            'name': self.game_name,
            'points_to_win':self.points_to_win,
            'stats': self.getGameStats(),
			'lobby': self.getLobby(),
        }

    def getGameStats(self):
        stats = self.stats.getUpdatedData()
        return stats
    
    def getLobby(self):  
        list_lobby = self.lobby_set.all()
        return list_lobby
