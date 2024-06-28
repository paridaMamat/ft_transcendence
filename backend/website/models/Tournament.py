from django.db import models
from django.utils import timezone
from django.http import JsonResponse
from typing import Any
# from .Party import PartyInTournament

#################################################
#                                               #
#             Tournament Class                  #
#                                               #
#################################################

class Tournament(models.Model):
    tour_name = models.CharField(max_length=15, blank=False, unique=False)
    tour_game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='tournament')
    tour_creator = models.ForeignKey('CustomUser', blank=False, on_delete=models.CASCADE)
    creation_date = models.DateField(auto_now=True)
    nb_rounds = models.IntegerField(default=2, blank=False)
    current_round = models.IntegerField(default=0)
    status = models.CharField(max_length=30, default='waiting')
    parties = models.ForeignKey('Party', blank=True, null=True, on_delete=models.CASCADE, related_name='tournament_party')
    nb_players = models.IntegerField(default=0)
    remaining_players = models.IntegerField(default=0)
    # start_time = models.DateTimeField(blank=True, null=True)
    # end_time = models.DateTimeField(blank=True, null=True)
    tour_users = models.ManyToManyField('CustomUser', related_name='tournaments', blank=True)
    tour_winner = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='tournament_winner', null=True)
    def __str__(self):
        return f"{self.tour_name} tournament {self.id} of {self.tour_game}"
    
    # @property     # -> permet d'acceder a l'attribut en lecture seule
    # def getNbUser(self):
    #     return self.tour_users.count()

    def getPlayersInfos(self):
        list_user = self.users.all()
        user = [user.getUserInfos() for user in list_user]
        return user
    
    def getPartiesFullInfos(self):
        parties = self.parties.all()
        return [party.getPartyData() for party in parties]
    
    # def getPartiesId(self):
    #     parties = self.party_set.all()
    #     return [party.id for party in parties]
  
    # def updateTourData(self):
    #     try:
    #         last_party = self.partyintournament_set.filter(round_nb=self.nb_rounds).get()
    #         # self.end_time = timezone.now()
    #         # self.duration = self.end_time - self.start_time
    #         self.status = 'finished'
    #         self.tour_winner = last_party.party.winner
    #         self.save()
    #         return JsonResponse({'status': 'ok', 'message': ('Tournament ended successfully.')})
    #     except PartyInTournament.DoesNotExist:
    #         return JsonResponse({'status': 'error', 'message': ('No last party found.')}, status=404)

    def getTourData(self):
        return {
            'id':self.id,
            'tour_name':self.tour_name,
            'tour_creator':self.tour_creator,
            'nb_rounds':self.nb_rounds,
            'parties':self.getPartiesFullInfos(),
            'nb_players':self.nb_players,
            'nb_rounds':self.nb_rounds,
            # 'duration':self.duration,
            'tour_users':self.getPlayersInfos(),
            'winner':self.tour_winner,
            'status':self.status,
        }