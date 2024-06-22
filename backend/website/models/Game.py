from django.db import models
from typing import Any

#############################################
#                                           #
#             Game Classes                  #
#                                           #
#############################################

class Game(models.Model):
    game_name = models.CharField(blank=False) # pong or memory
    #rules = models.TextField()
    point_to_win = models.IntegerField(default=5)
    def __str__(self):
        return f"{self.game_name}"

    def getGameData(self):
         return {
            'game_id':self.id,
            'name': self.game_name,
            #'rules':self.rules,
            'points_to_win':self.point_to_win,
            'stats': self.getGameStats(),
			'lobby': self.getLobby(),
			'tournament': self.getTournament()
        }

    def getGameStats(self):
        stats = self.stats.getUpdatedData()
        return stats
    
    def getLobby(self):  
        list_lobby = self.lobby_set.all()
        return list_lobby
    
    def getTournament(self):   # retrieve all the tournaments data from a Pong or Memory game
        list_tournament = self.tournament_set.all()
        tournament = [tournament.getTourData() for tournament in list_tournament]
        return tournament
    
    def getParties(self):   # retrieve all the parties data from a Pong or Memory game
        list_parties = self.party_set.filter(status='finished').order_by('-end_time')[:5]
        party = [party.getPartyData() for party in list_parties]
        return party

class GameStats(models.Model):
    game = models.OneToOneField(Game, on_delete=models.CASCADE, related_name='stats')
    parties_played = models.IntegerField(default=0)
    played_time = models.DateTimeField () #add the duration of all parties played
    avg_game_time = models.IntegerField() #calcul de la moyenne played_time / nb of parties_played    
    def __str__(self):
        return f"stat for {self.game} game {self.id}"
    
    def update(self, time: int):
        self.parties_played += 1
        self.played_time += time
        self.avg_game_time = self.played_time / self.parties_played    
        self.save()
    
    def getUpdatedData(self):
        return {
            'game':self.game,
            'parties_played': self.parties_played,
            'played_time':self.played_time,
            'avg_game_time':self.avg_game_time,
        }
