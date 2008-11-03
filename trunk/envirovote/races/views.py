from django.contrib.localflavor.us.us_states import STATE_CHOICES
from django.shortcuts import render_to_response
from races.models import Race
from endorsements.models import * 
from helpers import calculate_meter_info

def about(request):
    meter_info = calculate_meter_info(Race.objects.filter(year=2008))
    return render_to_response('about.html', {'meter_info':meter_info})

def index(request):
    key = Race.objects.filter(is_key=True)
    incoming = Race.objects.filter(year=2008,winner__isnull=False).order_by('-tally_updated')[:10]
    elections = get_elections()
    meter_info = calculate_meter_info(Race.objects.filter(year=2008))
    return render_to_response('index.html', {'key_races': key, 'incoming_races': incoming, 'meter_info': meter_info, 'elections': elections,})

def get_elections():
    elections = []
    for abbr, name in STATE_CHOICES:
        meter_info = calculate_meter_info(Race.objects.filter(year=2008,state=abbr))
        elections.append((name, meter_info))
    return elections
