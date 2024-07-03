from django.db import models
from django.utils import timezone
from typing import Any

##############################################
#                                            #
#             Party Classes                  #
#                                            #
##############################################

class Party(models.Model):
    game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='parties')
    player1 = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='player1')
    player2 = models.ForeignKey('CustomUser', related_name='party_player2', on_delete=models.CASCADE, null=True, blank=True)
    score1 = models.IntegerField(default=0)
    score2 = models.IntegerField(default=0)
    duration = models.IntegerField(default=0, blank=False)
    date = models.DateField(auto_now=True)
    winner_name = models.CharField(max_length=30, default='')
    status = models.CharField(default='waiting') #waiting, playing or finished
    tour = models.ForeignKey('Tournament', on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=30, default='Matchmaking') #sinon Tournament
    
    def __str__(self):
        return f"party {self.id} of game with player1 {self.player1} and player2 {self.player2}"
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
       super().__init__(*args, **kwargs)
       
    def getPartyData(self):
        return {
            'game':self.game,
            'player1': self.player1,
            'player2': self.player2,
            'score1': self.score1,
            'score2': self.score2,
            'duration':self.duration,
            'winner':self.winner_name,
        }
    