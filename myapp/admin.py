from django.contrib import admin

from .models import Bet, Wager

class BetAdmin(admin.ModelAdmin):
	list_display = ('title', 'key', 'date_created', 'date_accepted', 'creator_id')

admin.site.register(Bet, BetAdmin)
admin.site.register(Wager)


