from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from races.models import Race, STATE_CHOICES
from endorsements.models import * 
from races.helpers import *

def about(request):
    meter_info = calculate_meter_info(Race.objects.filter(year=2008))
    return render_to_response('about.html', {'meter_info':meter_info})

def state(request, election):
    return render_to_response('election.html')

def index(request):
    key = Race.objects.filter(is_key=True)
    incoming_races = Race.objects.filter(year=2008,winner__isnull=False).order_by('-tally_updated')[:10]
    states = get_states_and_info()
    meter_info = calculate_meter_info(Race.objects.filter(year=2008))
    return render_to_response('index.html', {'key_races': key, 'incoming_races': incoming_races, 'meter_info': meter_info, 'states': states,})
    
def detail(request,race_id):
    """detail on a race"""
    race = Race.objects.get(pk=race_id)
    candidates = race.candidate_set.order_by("-votes")
    return render_to_response('race_detail.html',{'race':race,'candidates':candidates})

def state(request, state):
    for abbr, name in STATE_CHOICES:
        if state == get_state_url_name(name):
            all_races = Race.objects.filter(year=2008,state=abbr)
            meter_info = calculate_meter_info(all_races)
            governor_races = Race.objects.filter(race_type='gov',year=2008,state=abbr)
            senate_races = Race.objects.filter(race_type='sen',year=2008,state=abbr)
            house_races = Race.objects.filter(race_type='hou',year=2008,state=abbr).order_by('district')
            return render_to_response('state.html',{'state':name, 'governor_races':governor_races, 'senate_races':senate_races, 'house_races':house_races, 'meter_info':meter_info,})
    return HttpResponseRedirect('/')

def embed(request):
    key = Race.objects.filter(is_key=True)
    incoming_races = Race.objects.filter(year=2008,winner__isnull=False).order_by('-tally_updated')[:10]
    states = get_states_and_info()
    meter_info = calculate_meter_info(Race.objects.filter(year=2008))
    return render_to_response('embedable.html', {'key_races': key, 'incoming_races': incoming_races, 'meter_info': meter_info, 'states': states,})