from django.contrib import admin
from envirovote.races.models import Candidate, Race

from django import forms

#idea from:
#http://www.fictitiousnonsense.com/archives/22
#http://oebfare.com/blog/2008/feb/23/changing-modelchoicefield-queryset/
class RaceAdminForm(forms.ModelForm):
    winner = forms.ModelChoiceField(queryset=Candidate.objects.none())

    def __init__(self, *args, **kwargs):
        super(RaceAdminForm, self).__init__(*args, **kwargs)
        self.fields["winner"].queryset = Candidate.objects.filter(race=self.instance).order_by('name')
        
class CandidateAdmin(admin.ModelAdmin):
    search_fields = ['name']
admin.site.register(Candidate, CandidateAdmin)

class RaceAdmin(admin.ModelAdmin):
    search_fields = ['year','district','race_type','state']
    form = RaceAdminForm
admin.site.register(Race, RaceAdmin)
