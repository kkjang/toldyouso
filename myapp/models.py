from django.db import models
from django.contrib.auth.models import User
import uuid

class Room(models.Model):
	user = models.ForeignKey(User, editable=False)
	date_created = models.DateField()
	room_key = models.UUIDField(default=uuid.uuid4, editable=False)
	title = models.CharField(max_length=255)
	ready = models.BooleanField()
	challenger_name = models.CharField(max_length=30)
	challenged_name = models.CharField(max_length=30)
	challenger_bet = models.TextField(max_length=255)
	challenged_bet = models.TextField(max_length=255)
	challenger_extra = models.CharField(max_length=100, blank=True)
	challenged_extra = models.CharField(max_length=100, blank=True)
