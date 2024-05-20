from django.db import models
from website.models import *
from django.utils import timezone
from django.http import JsonResponse
from typing import Any

#############################################
#                                           #
#             Game Classes                  #
#                                           #
#############################################

class Game(models.Model):
    game_name = models.CharField(blank=False) # pong or memory
    img = models.ImageField()
    description = models.TextField()
    rules = models.TextField()
    point_to_win = models.IntegerField(default=5)
    def __str__(self):
        return f"{self.game_name}"

    def getGameData(self):
         return {
            'game_id':self.id,
            'name': self.game_name,
            'image':self.img,
            'description':self.description,
            'rules':self.rules,
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
    game = models.OneToOneField('Game', on_delete=models.CASCADE, related_name='stats')
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

##############################################
#                                            #
#             Party Classes                  #
#                                            #
##############################################

class Party(models.Model):
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    game_name = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='game_name')
    player1 = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='player1')
    player2 = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='player2')
    score1= models.IntegerField(default=0)
    score2= models.IntegerField(default=0)
    start_time = models.DateTimeField (null=True, blank=True)
    end_time = models.DateTimeField (null=True, blank=True)
    duration = models.DateTimeField ()
    date = models.DateField(auto_now=True)
    winner = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    status = models.CharField(default='waiting') #waiting, playing or finished
    tour = models.ForeignKey('Tournament', on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=30, default='Matchmaking') #sinon Tournament
    def __str__(self):
        return f"party {self.id} of {self.game_name} game with player1 {self.player1} and player2 {self.player2}"
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
    
    def startParty(player1, player2, game, type):
        party = Party.objects.create(game=game, player1=player1, player2=player2)
        party.start_time = timezone.now()
        party.type = type
        party.save()
        return party
    
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

##############################################
#                                            #
#             Lobby Classes                  #
#                                            #
##############################################

class Lobby(models.Model):
    game = models.OneToOneField(Game, on_delete=models.CASCADE)
    users = models.ManyToManyField('website.CustomUser', through='UserInLobby', through_fields=('lobby', 'user'))
    def __str__(self):
        return f"lobby {self.id} for {self.game.game_name}"
    
    def getLobbyUsers(self):
        users_list = self.users.all()
        user = [user.id for user in users_list]
        return user

    def lobby_data(self):
        return {
            'id':self.id,
            'user': self.getLobbyUsers(),
        }
    
class UserInLobby(models.Model):
    user = models.ForeignKey('website.CustomUser', on_delete=models.CASCADE)
    lobby = models.ForeignKey(Lobby, on_delete=models.CASCADE)
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
    
#################################################
#                                               #
#             Tournament Class                  #
#                                               #
#################################################

class Tournament(models.Model):
    tour_name = models.CharField(blank=False, unique=False)
    tour_game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='tournament')
    tour_creator = models.ForeignKey('website.CustomUser', blank=False, on_delete=models.CASCADE)
    creation_date = models.DateField(auto_now=True)
    nb_rounds = models.IntegerField(default=2, blank=False)
    current_round = models.IntegerField(default=0)
    status = models.CharField(max_length=30, default='waiting')
    parties = models.ForeignKey('Party', blank=False, on_delete=models.CASCADE, related_name='Party')
    nb_players = models.IntegerField(default=0)
    remaining_players = models.IntegerField(default=0)
    start_time = models.DateTimeField ()
    end_time = models.DateTimeField ()
    duration = models.DateTimeField ()
    tour_users = models.ManyToManyField('website.CustomUser', related_name='tournaments')
    tour_winner = models.ForeignKey('website.CustomUser', on_delete=models.CASCADE, related_name='tournament_winner')
    def __str__(self):
        return f"{self.tour_name} tournament {self.id} of {self.tour_game}"
    
    @property     # -> permet d'acceder a l'attribut en lecture seule
    def getNbUser(self):
        return self.tour_users.count()

    def getPlayersInfos(self):
        list_user = self.users.all()
        user = [user.getUserInfos() for user in list_user]
        return user
    
    def getPartiesFullInfos(self):
        parties = self.parties.all()
        return [party.getPartyData() for party in parties]
    
    def getPartiesId(self):
        parties = self.party_set.all()
        return [party.id for party in parties]
 
    def updateTourData(self):
        try:
            last_party = self.partyintournament_set.filter(round_nb=self.nb_rounds).get()
            self.end_time = timezone.now()
            self.duration = self.end_time - self.start_time
            self.status = 'finished'
            self.tour_winner = last_party.party.winner
            self.save()
            return JsonResponse({'status': 'ok', 'message': ('Tournament ended successfully.')})
        except PartyInTournament.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': ('No last party found.')}, status=404)


    def getTourData(self):
        return {
            'id':self.id,
            'tour_name':self.tour_name,
            'tour_creator':self.tour_creator,
            'nb_rounds':self.nb_rounds,
            'parties':self.getPartiesFullInfos(),
            'nb_players':self.nb_players,
            'nb_rounds':self.nb_rounds,
            'duration':self.duration,
            'tour_users':self.getPlayersInfos(),
            'winner':self.tour_winner,
            'status':self.status,
        }

