from django.db import models
from django.contrib.auth.models import User
import uuid

class Wager(models.Model):
	condition = models.TextField(max_length=255)
	amount = models.CharField(max_length=100)
	user_id = models.ForeignKey(User, null=True)

class Bet(models.Model):
	title = models.CharField(max_length=255)
	key = models.UUIDField(default=uuid.uuid4, editable=False)
	date_created = models.DateField(auto_now_add=True, editable=False)
	wagers = models.ManyToManyField(Wager, blank=True)
	date_accepted = models.DateField(null=True)
	creator_id= models.ForeignKey(User, editable=False)


