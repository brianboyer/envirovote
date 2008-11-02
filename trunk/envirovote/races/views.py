from django.shortcuts import render_to_response
from races.models import Race
from endorsements.models import * 

def index(request):
    key = Race.objects.filter(is_key=True)
    incoming = Race.objects.filter(winner__isnull=False).order_by('-tally_updated')[:10]
    total_races = 0
    decided_races = 0
    green_races = 0
    for race in Race.objects.all():
        total_races += 1
        if race.winner:
            decided_races += 1
            if race.winner == race.greenest:
                green_races += 1
    percent_green = 100 * float(green_races) / float(decided_races)
    remaining_races = total_races - decided_races
    return render_to_response('index.html', {'key_races': key, 'incoming_races': incoming, 'decided_races': decided_races, 'green_races': green_races, 'percent_green': percent_green, 'remaining_races': remaining_races,})
