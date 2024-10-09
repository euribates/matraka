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
    tries = models.PositiveIntegerField(default=0)
    failures = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def load_or_create_score(cls, id_user, id_question):
        scores = (
            cls.objects
            .filter(question_id=id_question)
            .filter(user_id=id_user)
            )
        if scores.count() == 0:
            return cls(
                question_id=id_question,
                user_id=id_user,
                )
        return scores.first()

    def hits(self):
        return self.tries - self.failures


def user_failed_question(user, question):
    score = Score.load_or_create_score(user.pk, question.pk)
    score.tries += 1
    score.failures += 1
    score.save()


def user_passed_question(user, question):
    score = Score.load_or_create_score(user.pk, question.pk)
    score.tries += 1
    score.save()


def get_question_for_user(id_user):
    from django.db import connection
    sql = (
       'SELECT Q.id_question,'
       '       CASE'
       '         WHEN coalesce(tries, 0) < 4 THEN 64'
       '         WHEN failures * 4 > tries THEN 16'
       '         WHEN failures * 2 > tries THEN 4'
       '         ELSE 1'
       '        END AS weight'
       '  FROM questions_question Q'
       '  LEFT JOIN questions_score S'
       '         ON Q.id_question = S.question_id'
       '        AND user_id = %s'
       '  ORDER BY Q.id_question'
       )
    with connection.cursor() as cursor:
        cursor.execute(sql, [id_user])
        acc = 0
        population = []
        cum_weights = []
        for id_question, weight in cursor.fetchall():
            population.append(id_question)
            acc += weight
            cum_weights.append(acc)
    id_question = random.choices(population, cum_weights=cum_weights)
    return Question.load_question(id_question)
