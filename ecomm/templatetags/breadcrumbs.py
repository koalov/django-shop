from django import template
from ecomm.models import *

register = template.Library()


@register.inclusion_tag('breadcrumbs.html')
def get_breadcrumbs_product(curr_page):
    breadcrumbs = [curr_page.category, curr_page]
    return {'breadcrumbs_product': breadcrumbs}


@register.inclusion_tag('breadcrumbs.html')
def get_breadcrumbs_category(curr_page):
    breadcrumbs = curr_page.name
    return {'breadcrumbs_category': breadcrumbs}


@register.inclusion_tag('breadcrumbs.html')
def get_breadcrumbs_other(curr_page):
    breadcrumbs = curr_page
    return {'breadcrumbs_other': breadcrumbs}


