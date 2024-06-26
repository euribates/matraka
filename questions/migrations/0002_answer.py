# Generated by Django 5.0.6 on 2024-05-13 11:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("questions", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Answer",
            fields=[
                (
                    "id_answer",
                    models.BigIntegerField(primary_key=True, serialize=False),
                ),
                ("text", models.CharField(max_length=4096)),
                ("is_correct", models.BooleanField(default=False)),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="answers",
                        to="questions.question",
                    ),
                ),
            ],
        ),
    ]
