from django.contrib import admin
from envirovote.races.models import Candidate, Race

class CandidateAdmin(admin.ModelAdmin):
    search_fields = ['name']
admin.site.register(Candidate, CandidateAdmin)

class RaceAdmin(admin.ModelAdmin):
    search_fields = ['year','district','race_type','state']
admin.site.register(Race, RaceAdmin)
