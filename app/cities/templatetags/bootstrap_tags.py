from django import template
from django.http import HttpRequest

register = template.Library()


@register.simple_tag(takes_context=True)
def is_active_tab(context, *url_pattern_names):
    request: HttpRequest = context['request']

    app_name = request.resolver_match.app_name
    url_pattern_name = request.resolver_match.url_name

    for name in url_pattern_names:
        if f"{app_name}:{url_pattern_name}" == name:
            return 'active'
    return ''
