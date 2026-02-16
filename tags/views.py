#!/usr/bin/env python3

from django.db.models import Count
from django.shortcuts import render

from tags.models import Tag


def all_tags(request):
    """Muestra tocas las etiquetas.
    """
    tags = (
        Tag.objects.all()
        .annotate(num_questions=Count('questions'))
        )
    return render(request, 'tags/all_tags.html', {
        'num_tags': tags.count(),
        'tags': tags,
        })


def view_tag(request, tag_name: str):
    """Detalle de una etiqueta.
    """
    tag = Tag.load_tag(tag_name)
    return render(request, 'tags/view_tag.html', {
        'title': tag.name,
        'tag': tag,
        })
