from django.contrib.localflavor.us.us_states import STATE_CHOICES
from django.shortcuts import render_to_response
from races.models import Race
from endorsements.models import * 

def index(request):
    key = Race.objects.filter(is_key=True)
    incoming = Race.objects.filter(winner__isnull=False).order_by('-tally_updated')[:10]
    elections = get_elections()
    meter_info = get_meter_info(Race.objects.filter(year=2008))
    return render_to_response('index.html', {'key_races': key, 'incoming_races': incoming, 'meter_info': meter_info, 'elections': elections,})

def get_elections():
    elections = []
    for abbr, name in STATE_CHOICES:
        meter_info = get_meter_info(Race.objects.filter(year=2008,state=abbr))
        elections.append((name, meter_info))
    return elections

# all races must have a last_race, and all last_races must have a winner
# TODO what about two races w/o a greenest candidate?  it should work if they have a winner.
def get_meter_info(races):
    total_races = 0
    decided_races = 0
    green_races = 0
    previous_green_races = 0
    for race in races:
        total_races += 1
        if race.winner:
            decided_races += 1
            if race.winner == race.greenest:
                green_races += 1
            if race.last_race.winner == race.last_race.greenest:
                previous_green_races += 1
    if decided_races > 0:
        percent_green = 100 * float(green_races) / float(decided_races)
        percent_change = 100 * (float(green_races) - float(previous_green_races)) / float(decided_races)
    else:
        percent_green = 0
        percent_change = 0
    remaining_races = total_races - decided_races
    return {'decided_races': decided_races, 'green_races': green_races, 'percent_green': percent_green, 'percent_change': percent_change, 'remaining_races': remaining_races,}
    
        
        
