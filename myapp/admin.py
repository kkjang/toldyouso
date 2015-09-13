from django.contrib import admin

from .models import Room

class KeyAdmin(admin.ModelAdmin):
	readonly_fields = ('room_key',)

admin.site.register(Room, KeyAdmin)
