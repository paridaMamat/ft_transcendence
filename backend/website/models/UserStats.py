from django.db import models
from typing import Any
import logging

logger = logging.getLogger(__name__)

#################################################
#                                               #
#            User Stats Class                   #
#                                               #
#################################################

class UserStatsByGame(models.Model):
    game = models.ForeignKey('Game', blank=False, on_delete=models.CASCADE)#, related_name='name')
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, blank=False)
    time_played = models.IntegerField(default=0)
    avg_time_per_party = models.FloatField(default=0, blank=False)
    level = models.IntegerField(default=0, blank=False)
    score = models.IntegerField(default=0)
    played_parties = models.IntegerField(default=0)
    won_parties =  models.IntegerField(default=0)
    lost_parties =  models.IntegerField(default=0)
    parties_ratio = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    played_tour = models.IntegerField(default=0)
    won_tour = models.IntegerField(default=0)
    lost_tour = models.IntegerField(default=0)
    tour_ratio = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    def __str__(self):
        return f"{self.user} stats for {self.game}"
    
    def getPlayedParties(self):
        list_played_parties = self.played_parties.all()
        return list(list_played_parties)

    def updateUserData(self, time:int, party_winner:bool, tour:bool, tour_winner:bool, score:int): # tour_winner:bool
        self.played_parties += 1
        logger.debug("update nb parties: %s", self.played_parties)
        self.time_played += time
        self.avg_time_per_party = round(self.time_played / self.played_parties) if self.played_parties > 0 else 0
        logger.debug("avg_time_per_party: %s", self.avg_time_per_party)
        self.won_parties += party_winner
        self.lost_parties += self.played_parties - self.won_parties
        self.parties_ratio = self.won_parties / self.played_parties if self.played_parties > 0 else 0.0
        self.played_tour += tour
        self.won_tour += tour_winner
        self.lost_tour = self.played_tour - self.won_tour
        self.lost_parties = self.played_parties - self.won_parties
        self.tour_ratio = self.won_tour / self.played_tour if self.played_tour > 0 else 0.0
        self.score += score
        
        try:
            self.save()
            logger.debug("User data saved successfully.")
        except Exception as e:
            logger.error("Error saving user data: %s", e)

        logger.debug("Final state - played_parties: %s, won_parties: %s, lost_parties: %s, played_tour: %s, won_tour: %s, lost_tour: %s, score: %s", 
            self.played_parties, self.won_parties, self.lost_parties, self.played_tour, self.won_tour, self.lost_tour, self.score)


    def getUserDataGame(self):
        return {
            'id':self.id,
            'id_user': self.user.id,
            'id_game': self.game.id,
            'username':self.user.username,
            'avatar':self.user.avatar,
            'level':self.level,
            'score':self.score,
            'time':self.time_played,
            'avg_time':self.avg_time_per_party,
            'won_parties':self.won_parties,
            'lost_parties':self.lost_parties,
            'parties_ratio':self.parties_ratio,
            'core':self.score,
            'played_tour':self.played_tour,
            'won_tour':self.won_tour,
            'lost_tour':self.lost_tour,
        } 
        
    #def updateRank(self):
    ## Récupérer le nombre de parties jouées et gagnées
    #    nb_parties = self.nb_parties
    #    won_parties = self.won_parties

    #    # Calculer le ratio de parties gagnées
    #    if nb_parties == 0:
    #        ratio = 0.0
    #    else:
    #        ratio = won_parties / nb_parties

    #    # Déterminer le classement initial (ou le récupérer si existant)
    #    try:
    #        current_rank = self.rank
    #    except UserStatsByGame.DoesNotExist:
    #        current_rank = 1000  # Classement initial par défaut

    #    # Calculer le nouveau classement en utilisant le système Elo
    #    k = 32  # Facteur de classement (ajuster selon la précision souhaitée)
    #    base_rating = 1000  # Classement de base (ajuster selon la population de joueurs)
    #    expected_score = 1 / (1 + pow(10, (current_rank - base_rating) / 400))
    #    new_score = current_rank + k * (ratio - expected_score)

    #    # Mettre à jour le classement du joueur
    #    self.rank = int(round(new_score, 0))
    #    self.save()