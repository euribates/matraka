#!/usr/bin/env python3

from django.utils.safestring import mark_safe
from django import template
from django.urls import reverse

from tags.colors import Color

register = template.Library()


@register.filter
def as_tag(tag):
    luminance = tag.color.luminance()
    b_klass = 'badge-light' if luminance > 0.5 else 'badge-dark'
    url = reverse('tags:view_tag', kwargs={'tag_name': tag.name})  
    return mark_safe(
        '<span class="tag is-info"'
        f' title="{tag.description}"'
        f' style="background-color: {tag.color}">'
        f'<a class="badge {b_klass}" href="{url}">'
        f'{tag.name}'
        f'</a>'
        '</span>'
        )
