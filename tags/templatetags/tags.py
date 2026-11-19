#!/usr/bin/env python3

from django.utils.safestring import mark_safe
from django import template
from django.urls import reverse


register = template.Library()


@register.filter
def as_tag(tag):
    fg_color = tag.color.foreground_color()
    bg_color = tag.color.background_color()
    url = reverse('tags:view_tag', kwargs={'tag_name': tag.name})  
    return mark_safe(
        '<span class="tag is-info"'
        f' title="{tag.description}"'
        f' style="color: {fg_color}; background-color: {bg_color}">'
        f'<a class="badge" href="{url}">'
        f'{tag.name}'
        f'</a>'
        '</span>'
        )
