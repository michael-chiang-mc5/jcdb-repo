from django.template import Library
from MCBase.config_navbar import *
import re
from django.core.urlresolvers import reverse, NoReverseMatch
from datetime import datetime, timedelta, timezone
from django.utils.timesince import timesince
register = Library()

@register.filter
def age(value):
    now = datetime.now(timezone.utc)
    try:
        difference = now - value
    except:
        return "qwer"
        return value
    if difference <= timedelta(minutes=1):
        return 'just now'
    return '%(time)s ago' % {'time': timesince(value).split(', ')[0]}

# Returns a list containing range made from given value
# Usage (in template): {% for i in 3|get_range %}
@register.filter
def get_range( value ):
  return range( value )

@register.filter
def increment( i ):
  return i+1

@register.filter()
def zip_lists(a, b):
  return zip(a, b)

@register.inclusion_tag('MCBase/base-navbar.html', takes_context=True)
def load_base_navbar(context):
    navbar_variables = {'website_name': website_name,
                        'left_side_nav':left_side_nav,
                        'left_side_href':left_side_href,}
    context.update(navbar_variables)
    return context

# Usage:
#  <li class="nav-blog {% active 'url-name' %}"><a href="#">Home</a></li>
#  <li class="nav-blog {% active '^/regex/' %}"><a href="#">Blog</a></li>
@register.simple_tag(takes_context=True)
def active(context, pattern_or_urlname):
    try:
        pattern = '^' + reverse(pattern_or_urlname)
    except NoReverseMatch:
        pattern = pattern_or_urlname
    path = context['request'].path
    if re.search(pattern, path):
        return 'active'
    return ''
