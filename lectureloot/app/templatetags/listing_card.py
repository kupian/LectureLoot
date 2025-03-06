from django import template

register = template.Library()

@register.inclusion_tag('app/listing_card.html')
def render_listing(listing):
    return {'listing': listing}