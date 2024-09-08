#!/usr/bin/env python3


from django.contrib import admin

from tags.models import Tag


class TagAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_display = (
        'pk',
        'name',
        'color',
        'description',
        )


admin.site.register(Tag, TagAdmin)
