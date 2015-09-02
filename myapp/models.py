from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Statement(models.Model):
	statement_text = models.TextField()
	date_created = models.DateField()
	user = models.ForeignKey(User, unique=False)

	def __str(self):
		return self.statement_text
