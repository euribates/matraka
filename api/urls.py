#!/usr/bin/env python3

from django.urls import path
from . import views


def tie(ruta, vista, name=None):
    return path(ruta, vista, name=name or vista.__name__)


urlpatterns = [
    tie('', views.homepage),
    ]
