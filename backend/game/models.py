from django.db import models
from website.models import CustomUser
from typing import Any

class Game(models.Model):
    #game_id = models.AutoField(primary_key=True)
    game_name = models.CharField(blank=False) # pong or memory
    img = models.ImageField()
    description = models.TextField()
    rules = models.TextField()
    point_to_win = models.IntegerField(default=5)
    nb_parties_played = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.game_id}"

    def getGameData(self):
         return {
            'game_id':self.game_id,
            'name': self.game_name,
            'image':self.img,
            'description':self.description,
            'rules':self.rules,
            'points_to_win':self.point_to_win, 
        }

    def getGameStats(self):   #general metrics: nb of parties played
        return

class Party(models.Model):
    #game_id = models.AutoField(primary_key=True)
    players = models.ManyToManyField('website.CustomUser')
    #player2 = models.ManyToManyField(CustomUser, db_table='User/Game junction tab')
    start_time = models.DateTimeField ()
    end_time = models.DateTimeField ()
    duration = models.DateTimeField ()
    date = models.DateField(auto_now=True)
    winner = models.CharField(max_length=25, blank=False)

    def getPartyStats(self):
        return {
            'game_id':self.id,
            'players': self.getPlayers(),
            'duration':self.duration,
            'date':self.date,
            'winner':self.winner,
        }

    def getPlayers(self):
        return self.players.all()

    def method3(self):
        return

class PartyStats(models.Model):
    #party_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('website.CustomUser', on_delete=models.CASCADE) #one-to-many relationship
    game_id = models.ForeignKey(Party, on_delete=models.CASCADE) #one-to-many relationship
    won_set = models.IntegerField(default=0)
    lost_set = models.IntegerField(default=0)
    ratio = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    winner = models.BooleanField(default=False, blank=False)
    def __str__(self):
        return f"{self.party_id} party {self.game_id}"

    def getPartyStats(self):
         return {
            'party_id':self.party_id,
            #'user_id': self.user_id,
            'won_set':self.won_set,
            'lost_set':self.lost_set,
            'ratio':self.getRatio(),
            'score':self.score,
            'winner':self.winner,
        }
    
    def getRatio(self):
        self.ratio = self.won_set / self.lost_set * 100
        return self.ratio

class Lobby(models.Model):
    id = models.AutoField(primary_key=True)
    game = models.OneToOneField(Game, on_delete=models.CASCADE)
    users = models.ManyToManyField('website.CustomUser', through='UserInLobby', through_fields=('lobby', 'user'))
    
    def __str__(self):
        return f"lobby {self.id} for {self.ponggame.name}"

    def update_pong_data(self):
        return
    
class UserInLobby(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('website.CustomUser', on_delete=models.CASCADE)
    lobby = models.ForeignKey(Lobby, on_delete=models.CASCADE)
    entry_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.id} in lobby {self.lobby.id} since {self.entry_at}"
    
    def update_data(self):
        return {
            'id':self.id,
            'user': self.user,
            'lobby':self.lobby,
            'entry_at':self.entry_at,
        }

class Tournament(models.Model):
    #tour_id = models.AutoField(primary_key=True)
    tour_name = models.CharField(blank=False, unique=True)
    tour_game = models.CharField(blank=False) #pong or memory
    tour_creator = models.ForeignKey('website.CustomUser', blank=False, on_delete=models.CASCADE, related_name='created_tournaments')
    creation_date = models.DateField(auto_now=True)
    nb_rounds = models.IntegerField(default=5, blank=False)
    current_round = models.IntegerField()
    current_party = models.ForeignKey('Party', blank=False, on_delete=models.CASCADE)
    nb_players = models.IntegerField(default=0)
    start_time = models.DateTimeField ()
    end_time = models.DateTimeField ()
    duration = models.DateTimeField ()
    tour_users = models.ManyToManyField('website.CustomUser', related_name='participated_tournaments')
    winner = models.ForeignKey('website.CustomUser', on_delete=models.CASCADE, related_name='won_tournaments')
    def __str__(self):
        return f"{self.tour_name} tournament {self.tour_id}"
    
    def getTourPlayers(self):

        return

    def getRank(self):  # tab resuming the final ranking
        return

    def getTourStats(self):
        return
    
    def getTourDuration(self):
        self.duration = self.end_time - self.start_time
        return self.duration
