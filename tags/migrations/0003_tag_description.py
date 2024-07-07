# Generated by Django 5.0.6 on 2024-06-09 14:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tags", "0002_alter_tag_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="tag",
            name="description",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Textual description of label",
                max_length=255,
            ),
        ),
    ]