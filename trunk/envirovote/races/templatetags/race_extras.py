from django import template

register = template.Library()
    
@register.inclusion_tag('meter.html')
def show_meter(meter_info):
    return meter_info

@register.inclusion_tag('big_meter.html')
def show_big_meter(meter_info):
    return {'meter_info': meter_info}







