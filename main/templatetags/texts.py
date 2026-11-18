#!/usr/bin/env python3

import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def as_markdown(text: str) -> str:
    if not hasattr(as_markdown, 'md_processor'):
        as_markdown.md_processor = markdown.Markdown(
            extras=['tables', 'footnotes']
        )
    result = as_markdown.md_processor.convert(text)
    if '<table' in result:
        result = result.replace('<table', '<table class="table"')
    return mark_safe(result)
