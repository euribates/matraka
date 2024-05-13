#!/usr/bin/env python3

from django.contrib import admin
from questions.models import Question, Answer


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ('text', )
    list_display = ('id_question', 'text')


class AnswerAdmin(admin.ModelAdmin):
    search_fields = ('text', )
    list_display = ('id_answer', 'text', 'is_correct')


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
