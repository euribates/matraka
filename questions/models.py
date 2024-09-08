#!/usr/bin/env python3

import itertools
import random

from django.db import models
from django.urls import reverse_lazy
from django.conf import settings

from simple_history.models import HistoricalRecords

from sequtils import split_iter
from tags.models import Tag


class Question(models.Model):

    id_question = models.BigAutoField(primary_key=True)
    text = models.CharField(max_length=4096, unique=True)
    source = models.CharField(blank=True, default='', max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(
        Tag,
        related_name='questions',
        blank=True,
        )
    history = HistoricalRecords()

    @classmethod
    def load_question(cls, pk):
        try:
            return cls.objects.get(pk=pk)
        except cls.DoesNotExist:
            return None

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse_lazy('questions:question_detail', kwargs={
            'pk': self.pk,
            })

    def get_random_answers(self):
        valids, wrongs = split_iter(self.answers.all(), lambda _: _.is_correct)
        valids = list(valids)
        assert len(valids) >= 1
        wrongs = list(wrongs)
        assert len(wrongs) >= 3
        answers = [random.choice(valids)]
        answers.extend(list(random.sample(wrongs, 3)))
        random.shuffle(answers)
        return answers

    def get_variability(self):
        valids, wrongs = split_iter(self.answers.all(), lambda _: _.is_correct)
        n_valids = len(list(valids))
        n_wrongs = len(list(wrongs))
        result = n_valids * n_wrongs * (n_wrongs - 1) * (n_wrongs - 2) // 6
        return result
        # return '{} * {} * {} * {} // 6 == {}'.format(
            # n_valids,
            # n_wrongs,
            # n_wrongs - 1,
            # n_wrongs - 2,
            # result,
            # )




class Answer(models.Model):
    id_answer = models.BigAutoField(primary_key=True)
    question = models.ForeignKey(
        Question,
        on_delete=models.PROTECT,
        related_name='answers',
        )
    text = models.CharField(max_length=4096)
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    @classmethod
    def load_answer(cls, pk):
        try:
            return cls.objects.select_related('question').get(pk=pk)
        except cls.DoesNotExist:
            return None

    def __str__(self):
        return self.text


class Score(models.Model):

    class Meta:
        verbose_name = "Puntuación"
        verbose_name_plural = "Puntuaciones"
        unique_together = [
            ("user", "question"),
            ]

    id_score = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        )
    tries = models.PositiveIntegerField(default=1)
    failures = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
