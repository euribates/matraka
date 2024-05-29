#!/usr/bin/env python3

import random

from django.db import models
from django.urls import reverse_lazy

from sequtils import split_iter


class Question(models.Model):

    id_question = models.BigAutoField(primary_key=True)
    text = models.CharField(max_length=4096, unique=True)
    source = models.CharField(blank=True, default='', max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def load_question(cls, pk):
        try:
            return cls.objects.get(pk=pk)
        except cls.DoesNotExist:
            return None

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse_lazy('question_detail', kwargs={
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

    @classmethod
    def load_answer(cls, pk):
        try:
            return cls.objects.select_related('question').get(pk=pk)
        except cls.DoesNotExist:
            return None

    def __str__(self):
        return self.text





