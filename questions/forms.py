#!/usr/bin/env python3


from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Field

from questions.models import Question
from questions.models import Answer


class NewQuestionForm(ModelForm):
    """Formulario para el alta de preguntas.
    """

    class Meta:
        model = Question
        fields = ["text", "source"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'text',
            'source',
            Submit(
                'ok', 'Nueva pregunta',
                css_class='button is-white is-rouded',
                ),
        )


class EditQuestionForm(ModelForm):
    """Formulario para el alta de preguntas.
    """

    class Meta:
        model = Question
        fields = ["text", "source"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'text',
            'source',
            Submit(
                'ok', 'Editar pregunta',
                css_class='button is-white is-rouded',
                ),
        )


class NewAnswerForm(ModelForm):
    """Formulario para el alta de respuestas.
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


class EditAnswerForm(ModelForm):
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
