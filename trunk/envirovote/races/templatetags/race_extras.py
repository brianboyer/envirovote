from django import template
from races.models import Race, STATE_CHOICES
from races.helpers import get_states_and_info

register = template.Library()
    
@register.inclusion_tag('meter.html')
def show_meter(meter_info):
    return meter_info
    
@register.inclusion_tag('state_list.html')
def show_state_list():
    return {'states':get_states_and_info()}

@register.inclusion_tag('big_meter.html')
def show_big_meter(meter_info):
    return {'meter_info': meter_info}
    
@register.inclusion_tag('medium_meter.html')
def show_medium_meter(meter_info):
    return {'meter_info': meter_info}

@register.inclusion_tag('state_race.html')
def show_state_race(race):
    return {'race': race}

@register.inclusion_tag('race_short.html')
def show_race_short(race):
    return {'race': race}







