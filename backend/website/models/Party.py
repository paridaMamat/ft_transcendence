from django.db import models
from django.utils import timezone
from typing import Any

##############################################
#                                            #
#             Party Classes                  #
#                                            #
##############################################

class Party(models.Model):
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    game_name = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='game')
    player1 = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='player1')
    player2 = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='player2')
    score1= models.IntegerField(default=0)
    score2= models.IntegerField(default=0)
    start_time = models.DateTimeField (null=True, blank=True)
    end_time = models.DateTimeField (null=True, blank=True)
    duration = models.DateTimeField (default=0)
    date = models.DateField(auto_now=True)
    winner = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    status = models.CharField(default='waiting') #waiting, playing or finished
    tour = models.ForeignKey('Tournament', on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=30, default='Matchmaking') #sinon Tournament
    def __str__(self):
        return f"party {self.id} of {self.game_name} game with player1 {self.player1} and player2 {self.player2}"
    
    #def __init__(self, *args: Any, **kwargs: Any) -> None:
    #    super().__init__(*args, **kwargs)
    
    def startParty(player1, player2, game, type):
        party = Party.objects.create(game=game, player1=player1, player2=player2)
        party.start_time = timezone.now()
        party.type = type
        party.save()
        return party
    
    #def getLevel(self, level:int):
    #    return self.level.all()
    
    def updateEndParty(self):
        self.end_time = timezone.now()
        self.duration = self.end_time - self.start_time.seconds
        self.status = 'finished'
        if (self.score1 < self.score2):
            self.winner = self.player2
        elif (self.score1 > self.score2):
            self.winner = self.player1
        if self.tournament:
            party_in_tournament = PartyInTournament.objects.get(party=self)
            party_in_tournament.updateLastParty()
        self.save()
    
    def getPartyData(self):
        return {
            'game':self.game, #pong or memory
            'player1': self.player1,
            'player2': self.player2,
            'score1': self.score1,
            'score2': self.score2,
            'duration':self.duration,
            'winner':self.winner,
        }
    
class PartyInTournament(models.Model):
	party = models.OneToOneField('Party', on_delete=models.CASCADE)
	tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE)
	round_nb = models.IntegerField(default=0)
	index = models.IntegerField(default=0)
	def __str__(self):
		return f"Party {self.party} in tournament {self.tournament} for {self.round_nb} rounds"
	def updateLastParty(self):
		if self.index == self.tournament.nb_players/ (2**self.round_nb): #si c'est le dernier match de la ronde, c'est pas vraiment necessaire
				self.tournament.next_round(self.round_nb)
		self.save()