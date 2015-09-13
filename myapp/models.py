from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Statement(models.Model):
	statement_text = models.TextField()
	date_created = models.DateField()
	user = models.ForeignKey(User, unique=False)

	def __str(self):
		return self.statement_text

class Room(models.Model):
	date_created = models.DateField()
	room_key = models.UUIDField(default=uuid.uuid4, editable=False)
	title = models.CharField(max_length=255)
	ready = models.BooleanField()
	challenger_bet = models.TextField()
	challenged_bet = models.TextField()
