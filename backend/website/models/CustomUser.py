
import os
import uuid
from django.db import models
#from django.db.models import F
from django.contrib.auth.models import AbstractUser
from . import Game

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
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    rank = models.IntegerField(default=0, blank=False)
    status = models.CharField(max_length=7, default= 'online') #online, offline, playing
    friends = models.ManyToManyField('self')

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
    objects = models.Manager()
    def __str__(self):
        return f"{self.username}"
    
    def updateStatus(self, status: str):  #update of score/status/level
        self.status = status
        self.save()
     
    #def update_rank(self):
    #    try:
    #        stat_user = self.stat_user_by_game.get()
    #        stat_user.updateRank()
    #        stat_user.save()
    #    except UserStatsByGame.DoesNotExist:
    #        pass  # Ignorer si l'utilisateur n'a pas encore de statistiques de jeu

    #def save(self, *args, **kwargs):
    #    super().save(*args, **kwargs)
    #    self.update_rank() 
    
    def getUserInfos(self):  #update of score/status/level
        return {
            'user_id':self.id,
            'username': self.username,
            'avatar':self.avatar,
            'rank':self.rank,
            'status':self.status,
        }
    
    def getUserFullInfos(self):  #update of score/status/rank
         return {
            'user_id':self.id,
            'username': self.username,
            'avatar':self.avatar,
            'status':self.status,
            'email':self.email,
            'first_name':self.first_name,
            'last_name': self.last_name,
            'avatar':self.avatar,
            'rank':self.rank,
            'status':self.status,
            'date_j': self.date_joined,
            'friends': self.getFriends(),
			'friends_received': self.getFriendRequestReceived(),
			'request_sent': self.getFriendRequestSent(),
			'stat': self.getStat()
        }
    
    def getFriends(self):
        list_friends = self.friends.all()
        return [friend.getUserInfos() for friend in list_friends]

    def getFriendRequestReceived(self):
        list_friend_request = self.receiver.all()
        return [re.friend_request_data() for re in list_friend_request]

    def getFriendRequestSent(self):
        list_friend_request = self.sender.all()
        return [re.friend_request_data() for re in list_friend_request]

    def getStat(self):
        list_stat = self.stats.all()
        return [stat.getUserData() for stat in list_stat]

    def joinLobby(self, game_id: int):
        game = Game.objects.get(id=game_id)
        lobby = game.lobby
        if self in lobby.users.all():
            return game_id
        if self.lobby_set.count() > 0:
            return None
        lobby.users.add(self)
        return game_id

    def leaveLobby(self, game_id: int):
        game = Game.objects.get(id=game_id)
        lobby = game.lobby
        if self not in lobby.users.all():
            return None
        lobby.users.remove(self)
        return game_id

    def updateGameStat(self, game_id: int, time: int, win: bool, tour:bool, tour_winner:bool, score:int):
        game = Game.objects.get(id=id)
        stat = self.stats.get(game=game)
        stat.updateUserData(time, win, tour, tour_winner, score)
        return game_id
    
##############################################
#                                            #
#            Friends Class                   #
#                                            #
##############################################

class FriendRequest(models.Model):
	id = models.AutoField(primary_key=True)
	sender = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='sender')
	receiver = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='receiver')
	created_at = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return f"{self.sender} send friend request to {self.receiver}"
	
	def friend_request_data(self):
		return {
			'id': self.id,
			'sender': {
				'username': self.sender.username,
				'avatar': self.sender.avatar.url if self.sender.avatar else None,
			},
			'receiver': self.receiver.id,
			'message': f"You have a friend request from {self.sender.username}",
			'created_at': self.created_at,
		}
    

##################################################
#                                                #
#      function to retrieve avatars' file        #
#                                                #
##################################################

def get_file_path(instance, filename):
	ext = filename.split('.')[-1]
	filename = "%s.%s" % (uuid.uuid4(), ext)
	return os.path.join('avatars/', filename)
