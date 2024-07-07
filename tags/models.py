#!/usr/bin/env python3


from django.db import models

from tags.colors import Color
from tags.fields import ColorField


class Tag(models.Model):

    class Meta:
        ordering = ['name']

    id = models.BigAutoField(primary_key=True)
    name = models.SlugField(
        max_length=64,
        unique=True,
        )
    color = ColorField(
        default=Color.random_color,
        help_text='Label color in hex mode',
        )
    description = models.CharField(
        max_length=255,
        default='',
        unique=True,
        help_text='Textual description of label',
        )

    def __str__(self):
        return self.name

    @classmethod
    def load_tag(cls, slug):
        try:
            return cls.objects.get(name=slug)
        except cls.DoesNotExist:
            return None
