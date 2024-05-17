from django.db import models
from website.models import CustomUser
from django.utils import timezone
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
        return list_tournament
    
    def getParties(self):   # retrieve all the parties data from a Pong or Memory game
        list_parties = self.party_set.filter(status='finished').order_by('-end_time')[:5]
        party = [party.getPartyData() for party in list_parties]
        return list_parties

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
    game_name = models.ForeignKey('Gameme', on_delete=models.CASCADE, related_name='game_name')
    player1 = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='player1')
    player2 = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='player2')
    score1= models.IntegerField(default=0)
    score2= models.IntegerField(default=0)
    start_time = models.DateTimeField (null=True, blank=True)
    end_time = models.DateTimeField (null=True, blank=True)
    duration = models.DateTimeField ()
    date = models.DateField(auto_now=True)
    winner = models.CharField(max_length=25, blank=False)
    status = models.CharField(default='waiting') #waiting, playing or finished
    type = models.CharField(max_length=30, default='Matchmaking') #sinon Tournament
    
    def __str__(self):
        return f"party {self.id} of {self.game_name} game"
    
    def startParty(player1, player2, game, type):
        party = Party.objects.create(game=game, player1=player1, player2=player2)
        party.start_time = timezone.now()
        party.type = type
        party.save()
        return party
    
    def updatePartyData(self):
        self.end_time = timezone.now()
        self.duration = self.end_time - self.start_time
        self.status = 'finished'
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
    
#class PartyInTournament(models.Model):
#	id = models.AutoField(primary_key=True)
#	party = models.OneToOneField('Party', on_delete=models.CASCADE)
#	tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE)
#	round_nb = models.IntegerField(default=0)
#	index = models.IntegerField(default=0)
#	def __str__(self):
#		return f"Party {self.party} in tournament {self.tournament} for round {self.round_nb}"
#	def update_end(self):
#		if self.index == self.tournament.nb_player_to_start/ (2**self.round_nb): #si c'est le dernier match de la ronde, c'est pas vraiment necessaire
#				self.tournament.next_round(self.round_nb)
#		self.save()

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
        return f"{self.user.id} in lobby {self.lobby.id} since {self.entry_at}" 
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
    nb_rounds = models.IntegerField(default=5, blank=False)
    status = models.CharField(max_length=30, default='waiting')
    parties = models.ForeignKey('Party', blank=False, on_delete=models.CASCADE)
    nb_players = models.IntegerField(default=0)
    start_time = models.DateTimeField ()
    end_time = models.DateTimeField ()
    duration = models.DateTimeField ()
    tour_users = models.ManyToManyField('website.CustomUser', related_name='tournaments')
    tour_winner = models.ForeignKey('website.CustomUser', on_delete=models.CASCADE, related_name='tournament_winner')
    def __str__(self):
        return f"{self.tour_name} tournament {self.id} of {self.tour_game}"
    
    def getTourPlayers(self):
        list_players = self.tour_users.all()
        return list_players
    
    def getParties(self):
        parties = self.parties.all()
        return [party.getPartyData(minimal=True) for party in parties]
 
    def updateTourData(self):
        self.duration = self.end_time - self.start_time
        self.save()
        return

    def getTourData(self):
        return {
            'tour_name':self.tour_name,
            'tour_creator':self.tour_creator,
            'nb_rounds':self.nb_rounds,
            'parties':self.getParties(),
            'nb_players':self.nb_players,
            'duration':self.duration,
            'tour_users':self.getTourPlayers(),
            'winner':self.tour_winner,
        }
    
    def getTourDuration(self):
        self.duration = self.end_time - self.start_time
        return self.duration

##############################################
#                                            #
#             User's Stats Class             #
#                                            #
##############################################

#class Stat_User_by_Game(models.Model):  # allow to add player's history
#    game = models.ForeignKey('Game', blank=False, related_name='name')
#    user = models.ForeignKey('CustomUser', blank=False)
#    rank = models.IntegerField(default=0)
#    played_parties = models.IntegerField(default=0)
#    won_parties =  models.IntegerField(default=0)
#    parties_ratio = models.IntegerField(default=0)
#    highest_score = models.IntegerField(default=0)
#    lowest_score = models.IntegerField(default=0)
#    avg_score = models.IntegerField(default=0)
#    played_tour = models.IntegerField(default=0)
#    won_tour = models.IntegerField(default=0)
#    def __str__(self):
#        return f"{self.game}"
    
#    def getRank(self):  # tab resuming the final ranking
#        return
    
#    def getHighestScore(self):
#        return
    
#    def getLowestScore(self):
#        return
    
#    def getPartiesWon(self):
#        return
    
#    def getAvgScore(self):
#        return
    
#    def getWonTour(self):
#        return
    
#    def getPlayedParties(self):
#        return
    
#    def updateData(self):
#        self.played_parties = self.getPlayedParties()
#        self.won_parties = self.getPartiesWon()
#        self.parties_ratio = self.won_parties / self.played_parties * 100 # a affiner
#        self.highest_score = self.getHighestScore()
#        self.lowest_score = self.getHighestScore()
#        self.avg_score = self.getAvgScore()
#        self.rank = self.getRank()
#        self.won_tour = self.getWonTour()
#        self.save()

#    def getData(self):
#        return {
#            'id':self.id,
#            'user': self.user,
#            'rank':self.getRank(),
#            'won_parties':self.won_parties,
#            'parties_ratio':self.parties_ratio,
#            'highest_score':self.highest_score,
#            'avg_score':self.lowest_score, 
#            'score_ratio':self.score_ratio,
#            'played_tour':self.played_tour,
#            'won_tour':self.won_tour,
#        }