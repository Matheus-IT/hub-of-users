from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
	pass


class LoggedInUser(models.Model):
	""" Create a LoggedInUser instance when a user logs in, and the app will delete the instance
		when the user logs out """
	user = models.OneToOneField(
		settings.AUTH_USER_MODEL, 
		on_delete=models.CASCADE, 
		related_name='logged_in_user'
	)
