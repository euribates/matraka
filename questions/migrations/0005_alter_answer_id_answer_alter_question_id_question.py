# Generated by Django 5.0.6 on 2024-05-13 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("questions", "0004_answer_created_at_answer_updated_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="answer",
            name="id_answer",
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="question",
            name="id_question",
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
