from django import template
register = template.Library()

@register.filter
def index(indexable, i=85):
    return indexable[:i]