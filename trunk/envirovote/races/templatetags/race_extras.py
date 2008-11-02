from django import template

register = template.Library()
    
@register.inclusion_tag('meter.html')
def show_meter(percent_green):
    return {'percent_green': percent_green}







