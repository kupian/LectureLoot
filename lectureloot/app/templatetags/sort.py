from django import template

register = template.Library()

@register.inclusion_tag('app/sort.html')
def sort(results):
    return {'results': results}