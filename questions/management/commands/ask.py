#!/usr/bin/env python

import random
import textwrap

from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
from rich.panel import Panel
from django.core.management.base import BaseCommand

from sequtils import split_iter
from questions.models import Question


LETTERS = list('ABCD')
VALID_RESPONSES = LETTERS + ['Q']


class Command(BaseCommand):

    help = 'Índexar entradas del diccionario DC2'

    def __init__(self, *args, **kwargs):
        self.console = Console()
        super().__init__(*args, **kwargs)

    def out(self, *args, **kwargs):
        self.console.print(*args, **kwargs)

    def get_random_question(self):
        return random.choice(Question.objects.all())

    def handle(self, *args, **options):
        question = self.get_random_question()
        self.out(
            '[bold green]Matraka[/] quiere saber..\n\n',
            Markdown(f'# Pregunta {question.pk}\n\n'),
            Markdown(f'## {question.text}'),
            )
        answers = question.get_random_answers()
        table = Table()
        table.add_column("Letra", justify="right", style="bold", no_wrap=True)
        table.add_column("Respuesta")
        valid_matrix = {}
        for letter, answer in zip(LETTERS, answers):
            valid_matrix[letter] = answer
            table.add_row(letter, Markdown(answer.text))
        self.out(table)
        response = None
        while response not in VALID_RESPONSES:
            response = input(f'\nRespuesta: {VALID_RESPONSES!r}: ').upper()
        if response == 'Q':
            return
        answer = valid_matrix[response]
        if answer.is_correct:
            self.out('Muy bien, acertaste [green]:-)/]')
        else:
            self.out(
                'Lo siento, fallaste [red]:-([/]\n',
                'La respuesta correcta era:\n',
                Markdown(answer.text),
                response,
                )
