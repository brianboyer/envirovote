from django.shortcuts import render_to_response
from races.models import Race

def index(request):
    r = Race.objects.filter(is_key=True)
    return render_to_response('index.html', {'races': r,})
