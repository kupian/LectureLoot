from django import template

register = template.Library()

@register.inclusion_tag('app/sort_dropdown.html')
def sort_dropdown(sort_by=None):
    """
    render sorting dropdown for listings.
    
    parameters:
    sort_by (str): current sort option.
    """
    return {
        'sort_by': sort_by
    }