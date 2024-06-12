import json
from django.core.management.base import BaseCommand
from website.models.CustomUser import CustomUser
from website.models.UserStats import UserStatsByGame
from website.models.Lobby import Lobby
from website.models.Game import Game, GameStats
from website.models.Game import Game

class Command(BaseCommand):
    help = 'Load data from JSON file into the database'

    def handle(self, *args, **kwargs):
        with open('user_data.json') as file:
            data = json.load(file)
            for item in data:
                CustomUser.objects.create(**item)
                UserStatsByGame.objects.create(**item)
                Game.objects.create(**item)
        
        game1, _created = Game.objects.get_or_create(
			name='AI',
            points_to_win='5'
			# image='img/pong.jpg',
			# genre='Arcade, Sports, Action, Classic, Paddle, Simulation (Simple), Retro',
		)

        Game.objects.get_or_create(game=game1)
        Lobby.objects.get_or_create(game=game1)

        game2, _created = Game.objects.get_or_create(
			name='Pong',
            points_to_win='5'
			# image='img/pong.jpg',
			# genre='Arcade, Sports, Action, Classic, Paddle, Simulation (Simple), Retro',
		)

        Game.objects.get_or_create(game=game2)
        Lobby.objects.get_or_create(game=game2)

        game3, _created = Game.objects.get_or_create(
			name='memory',
            points_to_win='5'
			# image='img/pong.jpg',
			# genre='Arcade, Sports, Action, Classic, Paddle, Simulation (Simple), Retro',
		)

        Game.objects.get_or_create(game=game3)
        Lobby.objects.get_or_create(game=game3)

        #add some details to superuser
        superusers = CustomUser.objects.filter(is_superuser=True)
        if superusers:
            i = 0
            for user in superusers:
                user.first_name = 'Admin' + str(i)
                user.last_name = 'Transcendence'
                user.save()
                for game in Game.objects.all():
                    UserStatsByGame.objects.get_or_create(user=user, game=game)
				



    