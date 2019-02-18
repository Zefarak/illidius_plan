from django.contrib import admin

from .models import *


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    pass

@admin.register(Player, PlayerSeason, Game)
class MultiAdminData(admin.ModelAdmin):
    pass