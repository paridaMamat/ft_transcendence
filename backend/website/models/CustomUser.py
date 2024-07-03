
import os
import uuid
import json
from django.db import models
#from django.db.models import F
from django.contrib.auth.models import AbstractUser
from . import Game
from website.utils import get_file_path

# The User Model Django provides out of the box has some fields in general:
# username: The username that the user will use to authenticate. This will be unique in the table.
# email: The email that the user can choose to share. But out-of-the-box it is not unique.
# password1: The password user chooses to authenticate. It is not a plain password. It will be hashed for security reasons.
# password2: This is used to confirm passwords. On the Admin side, only one field named password is seen.
# first_name: The first name of the person.
# last_name: The last name of the person.
# last_login: The last Date and Time the user logged in.
# date_joined: The Date and Time the user joined/authenticated with your website.
# groups: The groups the user is in.
# user_permissions: Admin permissions if any.
# is_staff: Designates whether the user can log into the admin site.
# is_active: Designates whether this user should be treated as active. Unselect this instead of deleting accounts.
# is_superuser: Designates that this user has all permissions without explicitly assigning them.

#################################################
#                                               #
#             CustomUser Class                  #
#                                               #
#################################################

class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to=get_file_path, default='avatars/default-avatar.jpg')
    alias = models.CharField(max_length=15, default='', blank=False)
    status = models.CharField(max_length=15, default= 'online') #online, offline, playing, waiting
    friends = models.ManyToManyField('self')
    two_factor_enabled = models.BooleanField(default=False)  # Field to indicate if 2FA is enabled
    two_factor_secret = models.CharField(max_length=100, null=True, blank=True)  # Field to store 2FA secret key
    #stats = models.ForeignKey('UserStatsByGame', on_delete=models.CASCADE)

    # Add related_name for groups and user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_user_set',
        related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_set',
        related_query_name='custom_user',
        help_text='Specific permissions for this user.',
    )
    #objects = models.Manager()
    def __str__(self):
        return f"{self.username}"
    
    def updateStatus(self, status: str):  #update of score/status/level
        self.status = status
        self.save()
    
    def getUserInfo(self):  #update of score/status/level
        return {
            'user_id':self.id,
            'username': self.username,
            'avatar': self.avatar.url if self.avatar else None,
            'status':self.status,
        }
    
    def getUserFullInfos(self):  #update of score/status/level
         return {
            'user_id':self.id,
            'username': self.username,
            'avatar': self.avatar.url if self.avatar else None,
            'alias':self.getAlias,
            'email':self.email,
            'level':self.level,
            'first_name':self.first_name,
            'last_name': self.last_name,
            'status':self.status,
            'date_joined': self.date_joined,
            'friends': self.getFriends(),
			'stats': self.getStat()
        }
    
    def getFriends(self):
        list_friends = self.friends.all()
        return [friend.getUserInfo() for friend in list_friends]

    def getStat(self):
        list_stat = self.stats.all()
        return [stats.getUserDataGame() for stats in list_stat]
    
    def getAlias(self):
        user = self.alias
        if user is None:
            user = self.username
        return user

    def updateGameStat(self, game_id: int, time: int, win: bool, tour:bool, tour_winner:bool, score:int):
        game = Game.objects.get(id=id)
        stat = self.stats.get(game=game)
        stat.updateUserData(time, win, tour, tour_winner, score)
        return game_id
