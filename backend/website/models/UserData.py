
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    score = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    status = models.CharField(max_length=8, default= 'online') #online, offline, playing
    list_friends = models.ManyToManyField('self')

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
        return self.username
    
    def add_friends(self):
        return

    def edit_profil(self):  #change of names/avatar etc
        return

    def update_profil(self):  #update of score/status/level
        return

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


#	PARAM DE MODELS
#		primary_key
#		unique
#		default
#		null
#		blank
#		on_delete
	
#	ATTRIBUTS DE MODELS
#		CharField
#		IntegerField
#		DateField
#		FloatField
#		EmailField
#		BooleanField
