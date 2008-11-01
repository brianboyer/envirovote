from django.contrib import admin
from envirovote.races.models import Candidate, Race

class CandidateAdmin(admin.ModelAdmin):
    pass
admin.site.register(Candidate, CandidateAdmin)

class RaceAdmin(admin.ModelAdmin):
    pass
admin.site.register(Race, RaceAdmin)
