from django import template
register = template.Library()

@register.inclusion_tag('pagination.html')
def show_pagination(items):
    return {'items': items}
