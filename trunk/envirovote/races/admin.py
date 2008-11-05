from django.contrib import admin
from envirovote.races.models import Candidate, Race
from datetime import datetime


from django import forms

#idea from:
#http://www.fictitiousnonsense.com/archives/22
#http://oebfare.com/blog/2008/feb/23/changing-modelchoicefield-queryset/
class RaceAdminForm(forms.ModelForm):
    winner = forms.ModelChoiceField(queryset=Candidate.objects.none())

    def __init__(self, *args, **kwargs):
        super(RaceAdminForm, self).__init__(*args, **kwargs)
        self.fields["tally_updated"] = datetime.now()
        self.fields["last_race"].queryset = Race.objects.filter(year__lt='2008',race_type=self.instance.race_type,district=self.instance.district,state=self.instance.state)
        self.fields["winner"].queryset = Candidate.objects.filter(race=self.instance).order_by('name')
        
class CandidateAdmin(admin.ModelAdmin):
    search_fields = ['name']
admin.site.register(Candidate, CandidateAdmin)

class RaceAdmin(admin.ModelAdmin):
    search_fields = ['year','district','race_type','state']
    form = RaceAdminForm
admin.site.register(Race, RaceAdmin)
