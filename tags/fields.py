#!/usr/bin/env python3

from django.db import models

from tags.colors import Color
from tags.colors import get_rgb_from_hex, get_hex_from_rgb


class ColorField(models.CharField):
    """Custom Field to store colors as RGB Html values #RRGGBB.
    """

    description = "Field for colors"

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 7
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["max_length"]
        return name, path, args, kwargs

    def db_type(self, connection):
        return "char(7)"

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        red, green, blue = get_rgb_from_hex(value)
        return Color(red, green, blue)

    def to_python(self, value):
        if isinstance(value, Color):
            return value
        if value is None:
            return None
        red, green, blue = get_rgb_from_hex(value)
        return Color(red, green, blue)

    def get_prep_value(self, value):
        if value:
            return str(value)
        return ''
