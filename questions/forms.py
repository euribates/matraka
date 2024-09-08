#!/usr/bin/env python3

from django.urls import reverse_lazy
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div
from crispy_forms.layout import Field
from crispy_forms.layout import Layout
from crispy_forms.layout import Submit

from questions.models import Question
from questions.models import Answer


class NewQuestionForm(forms.ModelForm):
    """Formulario para el alta de preguntas.
    """

    class Meta:
        model = Question
        fields = ["text", "source", "tags"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'text',
            'source',
            'tags',
            Submit(
                'ok', 'Nueva pregunta',
                css_class='button is-white is-rouded',
                ),
        )
        self.fields['text'].widget = forms.Textarea(attrs={
            'cols': 80,
            'rows': 3,
            })


class EditQuestionForm(forms.ModelForm):
    """Formulario para el alta de preguntas.
    """

    class Meta:
        model = Question
        fields = ["text", "source", "tags"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'text',
            'source',
            'tags',
            Submit(
                'ok', 'Editar pregunta',
                css_class='button is-white is-rouded',
                ),
        )
        self.fields['text'].widget = forms.Textarea(attrs={
            'cols': 80,
            'rows': 3,
            })


class NewAnswerForm(forms.ModelForm):
    """Formulario para el alta de respuestas.
    """

    class Meta:
        model = Answer
        fields = ["text", "is_correct"]

    def __init__(self, question, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.question = question
        self.helper = FormHelper()
        self.helper.form_action = reverse_lazy('questions:new_answer', kwargs={
            'pk': self.question.pk,
            })
        self.helper.layout = Layout(
            'text',
            'is_correct',
            Submit(
                'ok', 'Nueva respuesta',
                css_class='button is-white is-rouded',
                ),
        )
        self.fields['text'].widget = forms.Textarea(attrs={
            'cols': 80,
            'rows': 3,
            })

    def save(self, *args, **kwargs):
        answer = super().save(commit=False)
        answer.question = self.question
        answer = super().save(*args, **kwargs)
        return answer


class EditAnswerForm(forms.ModelForm):
    """Formulario para la edición de las respuestas.
    """

    class Meta:
        model = Answer
        fields = ["question", "text", "is_correct"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = '.'
        self.helper.layout = Layout(
            Field('question', type="hidden"),
            'text',
            'is_correct',
            Submit(
                'ok', 'Nueva respuesta',
                css_class='button is-white is-rouded',
                ),
        )
        self.fields['text'].widget = forms.Textarea(attrs={
            'cols': 80,
            'rows': 3,
            })


class SearchForm(forms.Form):

    query = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = reverse_lazy('search')
        self.helper.layout = Div(
            Field('query'),
            Submit(
                'ok', 'Buscar',
                css_class='button is-white is-rouded',
                ),
            css_class='field',
            )


class AskForm(forms.Form):
    CHOICES = list(zip('ABCD', 'ABCD'))

    letter = forms.ChoiceField(choices=CHOICES)

    def clean_letter(self):
        _data = self.cleaned_data["letter"].upper()
        return _data.strip()
