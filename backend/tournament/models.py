from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class TournamentMatch(models.Model) :
	player1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="player1", blank=True, null=True)
	player2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="player2", blank=True, null=True)
	winner = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="winner", blank=True, null=True)
	round = models.IntegerField(default=1)
	match_id = models.IntegerField(default=1)

	def __str__(self):
		return self.player1.name + " vs " + self.player2.name

class Tournament(models.Model) :
	name = models.CharField(max_length=100)
	players = models.ManyToManyField(Player, blank=True)
	matchs = models.ManyToManyField(TournamentMatch, blank=True)
	online = models.BooleanField(default=False)
	rounds = models.IntegerField(default=1)
	current_round = models.IntegerField(default=1)
	finished = models.BooleanField(default=False)

	def __str__(self):
		return self.name
	class Meta:
		app_label = "tournament"

