from django import template
from django.http import HttpRequest
from django.utils.html import format_html

register = template.Library()


@register.simple_tag(takes_context=True)
def is_active_tab(context, *url_pattern_names):
    request: HttpRequest = context.get('request')

    if request.resolver_match:
        app_name = request.resolver_match.app_name
        url_pattern_name = request.resolver_match.url_name

        for name in url_pattern_names:
            if f"{app_name}:{url_pattern_name}" == name:
                return 'active'
    return ''


@register.simple_tag()
def message_icon(tag):
    icons = {
        'alert': '<i class="bi bi-info-circle-fill"></i>',
        'success': '<i class="bi bi-check-circle-fill"></i>',
        'warning': '<i class="bi bi-exclamation-circle-fill"></i>',
        'danger': '<i class="bi bi-exclamation-triangle-fill"></i>',
    }
    return format_html(icons.get(tag, icons['alert']))
