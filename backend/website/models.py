
import os
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from game import *

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
    score = models.IntegerField(default=0)
    pong_rank = models.IntegerField(default=0)
    AI_rank = models.IntegerField(default=0)
    memo_rank = models.IntegerField(default=0)
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
    def __str__(self):
        return f"{self.username}"
    
    def update_status(self, status: str):  #update of score/status/level
        self.status = status
        return self.save()
    
    def get_user_infos(self):  #update of score/status/level
        return {
            'user_id':self.id,
            'username': self.username,
            'avatar':self.avatar,
            'pong_rank':self.pong_rank,
            'AI_rank':self.AI_rank,
            'memo_rank':self.memo_rank,
            'status':self.status,
        }
    
    def get_user_full_infos(self):  #update of score/status/rank
         return {
            'user_id':self.id,
            'username': self.username,
            'avatar':self.avatar,
            'rank':self.rank,
            'status':self.status,
            'friends':list(self.friends.all()),
            'email':self.email,
            'first_name':self.first_name,
            'last_name': self.last_name,
            'avatar':self.avatar,
            'pong_rank':self.pong_rank,
            'AI_rank':self.AI_rank,
            'memo_rank':self.memo_rank,
            'status':self.status,
            'date_joined': self.date_joined,
        }
    
    #def getFriends(self):
    #    list_friends = self.friends.all()
    #    return [friend.user_data(minimal=True) for friend in list_friends]

    #def getFriendRequestReceived(self):
    #    list_friend_request = self.receiver.all()
    #    return [re.friend_request_data() for re in list_friend_request]

    #def getFriendRequestSent(self):
    #    list_friend_request = self.sender.all()
    #    return [re.friend_request_data() for re in list_friend_request]

    #def getStat(self):
    #    list_stat = self.stats.all()
    #    return [stat.stat_user_by_game_data() for stat in list_stat]
    
#################################################
#                                               #
#            User Stats Class                   #
#                                               #
#################################################

class Stat_User_by_Game(models.Model):
    game = models.ForeignKey('Game', blank=False, related_name='name')
    user = models.ForeignKey('CustomUser', blank=False)
    rank = models.IntegerField(default=0)
    played_parties = models.IntegerField(default=0)
    won_parties =  models.IntegerField(default=0)
    parties_ratio = models.IntegerField(default=0)
    highest_score = models.IntegerField(default=0)
    lowest_score = models.IntegerField(default=0)
    avg_score = models.IntegerField(default=0)
    played_tour = models.IntegerField(default=0)
    won_tour = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.user} stats for {self.game}"
    
    def getRank(self):  # tab resuming the final ranking
        return
    
    def getHighestScore(self):
        return
    
    def getLowestScore(self):
        return
    
    def getPartiesWon(self):
        return
    
    def getAvgScore(self):
        return
    
    def getWonTour(self):
        return
    
    def getPlayedParties(self):
        return
    
    def updateData(self):
        self.played_parties = self.getPlayedParties()
        self.won_parties = self.getPartiesWon()
        self.parties_ratio = self.won_parties / self.played_parties * 100 # a affiner
        self.highest_score = self.getHighestScore()
        self.lowest_score = self.getHighestScore()
        self.avg_score = self.getAvgScore()
        self.rank = self.getRank()
        self.won_tour = self.getWonTour()
        self.save()

    def getData(self):
        return {
            'id':self.id,
            'user': self.user,
            'rank':self.getRank(),
            'won_parties':self.won_parties,
            'parties_ratio':self.parties_ratio,
            'highest_score':self.highest_score,
            'avg_score':self.lowest_score, 
            'score_ratio':self.score_ratio,
            'played_tour':self.played_tour,
            'won_tour':self.won_tour,
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
