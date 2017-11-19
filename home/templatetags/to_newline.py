from django import template

register = template.Library()


@register.filter
def to_newline(value):
    return str(value).replace("\n", "<br />")
