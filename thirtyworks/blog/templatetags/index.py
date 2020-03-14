from django import template
register = template.Library()

@register.filter
def insta(indexable, i):
    return indexable[i].insta_handler 

@register.filter
def url(indexable, i):
    return indexable[i].url