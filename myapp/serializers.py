from .models import Room
from rest_framework import serializers
from django.contrib.auth.models import User


class RoomSerializer(serializers.ModelSerializer):
	class Meta:
		model = Room
		fields = '__all__'