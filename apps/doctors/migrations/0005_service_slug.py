# Generated by Django 5.0.6 on 2024-06-29 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0004_alter_direction_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='slug',
            field=models.SlugField(blank=True, default=None, null=True, unique=True),
        ),
    ]