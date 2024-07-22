#!/usr/bin/env python3

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div
from crispy_forms.layout import Field
from crispy_forms.layout import Layout
from crispy_forms.layout import Submit


class LoginForm(forms.Form):
    username = forms.SlugField(
        max_length=64,
        required=True,
        label='Username',
        help_text='Identificador del usuario',
        )
    password = forms.CharField(
        max_length=64,
        required=True,
        label='Password',
        help_text='Contraseña',
        widget=forms.widgets.PasswordInput,
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div('username'),
            Div('password'),
            Submit(
                'ok', 'Log in',
                css_class='button is-white is-rouded',
                ),
            )
