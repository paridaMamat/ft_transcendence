import json
from django.core.management.base import BaseCommand
from website.models.CustomUser import CustomUser
from website.models.UserStats import UserStatsByGame
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
    