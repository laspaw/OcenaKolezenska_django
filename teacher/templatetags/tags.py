from django import template

register = template.Library()


@register.simple_tag
def set(value=None):
    return value
