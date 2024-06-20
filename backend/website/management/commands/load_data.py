import json
from django.core.management.base import BaseCommand
from website.models.CustomUser import CustomUser
from website.models.UserStats import UserStatsByGame
from website.models.Lobby import Lobby
from website.models.Game import Game

class Command(BaseCommand):
    help = 'Load data from JSON file into the database'

    def handle(self, *args, **kwargs):
        try:
            with open('user_data.json', 'r') as file:
                data = json.load(file)
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            for item in data:
                CustomUser.objects.create(**item)
                UserStatsByGame.objects.create(**item)
                Game.objects.create(**item)
				