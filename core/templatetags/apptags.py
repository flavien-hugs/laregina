from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def active_nav(context, name):
    if context["request"].resolver_match.url_name == name:
        return "active"
    return ""
