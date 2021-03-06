from .models import Bet, Wager
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.response import Response


class WagerSerializer(serializers.ModelSerializer):
	user_id = serializers.PrimaryKeyRelatedField(required=False, read_only=True)

	class Meta:
		model = Wager
		fields = '__all__'

class BetSerializer(serializers.ModelSerializer):
	wagers = WagerSerializer(many=True, read_only=True)
	wager_data = serializers.JSONField(required=False)
	creator_id = serializers.PrimaryKeyRelatedField(required=False, read_only=True)

	class Meta:
		model = Bet
		fields = '__all__'

	def create(self, validated_data):
		request = self.context['request']
		wager_data = validated_data.pop('wager_data')
		created_wager = []
		for num, wager in enumerate(wager_data):
			wager = WagerSerializer(data=wager)
			if wager.is_valid():
				if num == 0:
					wager.save(user_id=request.user)
				created_wager.append(wager.save())
			else:
				return Response(wager.errors, status=status.HTTP_400_BAD_REQUEST)

		bet = Bet.objects.create(**validated_data)
		for wager in created_wager:
			bet.wagers.add(wager)
		return bet
