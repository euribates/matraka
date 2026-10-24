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
        'titulo': 'Todas las etiquetas',
        'num_tags': tags.count(),
        'tags': tags,
        })


def view_tag(request, tag_name: str):
    """Detalle de una etiqueta.
    """
    tag = Tag.load_tag(tag_name)
    questions = tag.questions.all()
    num_questions = questions.count()
    return render(request, 'tags/view_tag.html', {
        'titulo': (
            f"Preguntas etiquetas como {tag.name}"
            f" ({num_questions})"
            ),
        'tag': tag,
        'questions': questions,
        'num_questions': num_questions,
        })
