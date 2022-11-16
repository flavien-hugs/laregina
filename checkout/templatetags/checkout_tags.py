# order.templatetags.checkout_tags.py

from django import template

register = template.Library()


@register.inclusion_tag("checkout/snippet/form.html")
def form_table_row(form_field):
    return {"form_field": form_field}
