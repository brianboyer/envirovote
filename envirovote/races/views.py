from django.shortcuts import render_to_response
from races.models import Race

def index(request):
    key = Race.objects.filter(is_key=True)
    incoming = Race.objects.filter(winner__isnull=False).order_by('-tally_updated')[:10]
    return render_to_response('index.html', {'key_races': key, 'incoming_races': incoming,})
