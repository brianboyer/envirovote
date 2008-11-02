from django import template

register = template.Library()
    
@register.inclusion_tag('meter.html')
def show_meter(meter_info):
    return meter_info







