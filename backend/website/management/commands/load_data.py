import json
from django.core.management.base import BaseCommand
from website.models.CustomUser import CustomUser
from website.models.UserStats import UserStatsByGame
<<<<<<< HEAD
from website.models.Lobby import Lobby
=======
>>>>>>> origin/Barbara
from website.models.Game import Game

class Command(BaseCommand):
    help = 'Load data from JSON file into the database'

    def handle(self, *args, **kwargs):
<<<<<<< HEAD
        with open('user_data.json') as file:
            data = json.load(file)
=======
        try:
            with open('user_data.json', 'r') as file:
                data = json.load(file)
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
>>>>>>> origin/Barbara
            for item in data:
                CustomUser.objects.create(**item)
                UserStatsByGame.objects.create(**item)
                Game.objects.create(**item)
<<<<<<< HEAD
    
        game1, _created = Game.objects.get_or_create(
			name='PongAI',
			# image='img/pong.jpg',
			# genre='Arcade, Sports, Action, Classic, Paddle, Simulation (Simple), Retro',
			
		)

        UserStatsByGame.objects.get_or_create(game=game1)

        game2, _created = Game.objects.get_or_create(
			name='Pong',
			# image='img/pong.jpg',
			# genre='Arcade, Sports, Action, Classic, Paddle, Simulation (Simple), Retro',
			
		)

        UserStatsByGame.objects.get_or_create(game=game2)
        Lobby.objects.get_or_create(game=game2)

		# description_tictactoe = """
		# Tic Tac Toe, also known as Naughts and Crosses, is a classic two-player game.
		# Players take turns marking spaces in a 3x3 grid, aiming to form a row, column, or diagonal of their symbol (X or O).
		# Simple yet strategic, it's a timeless test of wit and tactics.
		# """
		# rule_tictactoe = """
		# The game is played on a 3x3 grid.
		# Players take turns marking an empty cell with their symbol (X or O).
		# The first player to form a row, column, or diagonal of their symbol wins the game.
		# In tournament mode, it's a draw, the first player loses.
		# """

        game3, _created = Game.objects.get_or_create(
			name='Memory',
			# image='img/tictactoe1.webp',
			# description=description_tictactoe,
			# genre='Puzzle, Board Game, Strategy',
			# rules=rule_tictactoe,
		)

        UserStatsByGame.objects.get_or_create(game=game3)
        Lobby.objects.get_or_create(game=game3)

	#add some details to superuser
        superusers = CustomUser.objects.filter(is_superuser=True)
        if superusers:
            i = 0
            for user in superusers:
                user.first_name = 'Admin' + str(i)
                user.last_name = 'Transcendence'
                user.sexe = 'F'
                user.birth_date = "1990-01-01"
                user.save()
                for game in Game.objects.all():
                    UserStatsByGame.objects.get_or_create(user=user, game=game)
=======
>>>>>>> origin/Barbara
				