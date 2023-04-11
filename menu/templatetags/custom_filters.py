from django import template

register = template.Library()

@register.filter(name='repeat')
def repeat(value, times):
    return value * times