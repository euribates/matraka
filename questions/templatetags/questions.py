#!/usr/bin/env python3


from django import template

register = template.Library()


IS_YES = '<strong class="boolean yes" style="color: #18442D">\u2705</strong>'

IS_NO = '<strong class="boolean no" style="color: #321A22">\u274C</strong>'


@register.filter
def as_bool(value: bool):
    return IS_YES if value else IS_NO
