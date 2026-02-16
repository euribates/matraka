#!/usr/bin/env python3

from django.utils.safestring import mark_safe
from django import template

register = template.Library()


@register.filter
def as_tag(tag):
    fg_color = tag.color.foreground_color()
    bg_color = tag.color.background_color()
    return mark_safe(
        '<span class="tag is-info"'
        f' title="{tag.description}"'
        f' style="color: {fg_color}; background-color: {bg_color}">'
        f'{tag.name}'
        '</span>'
        )
