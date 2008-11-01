from django.contrib import admin
from envirovote.races.models import Race

class RaceAdmin(admin.ModelAdmin):
    pass

admin.site.register(Race, RaceAdmin)
