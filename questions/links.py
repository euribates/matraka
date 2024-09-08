#!/usr/bin/env python3

"""
Funciones para obtener URLs

La idea es tener todas las llamadas a reverse_lazy o reverse
en un único lugar.

Todas las funciones deberían seguir la nomemclatura `a_<nombre-de-la-vista>`.
"""

from django.urls import reverse_lazy


def a_question_detail(id_question: int):
    """Devuelve la URL de la vista de detalles de una pregunta.
    """
    return reverse_lazy(
        'questions:question_detail',
        kwargs={'pk': id_question},
        )
