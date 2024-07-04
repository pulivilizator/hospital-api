# Generated by Django 5.0.6 on 2024-06-27 20:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Direction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Направление',
                'verbose_name_plural': 'Направления',
            },
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specialty', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('direction', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='doctors', to='doctors.direction')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Доктор',
                'verbose_name_plural': 'Доктора',
                'indexes': [models.Index(fields=['specialty'], name='doctors_doc_special_4b2702_idx'), models.Index(fields=['user'], name='doctors_doc_user_id_615418_idx')],
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('direction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='doctors.direction')),
            ],
            options={
                'verbose_name': 'Услуга',
                'verbose_name_plural': 'Услуги',
                'indexes': [models.Index(fields=['name'], name='doctors_ser_name_32cf31_idx'), models.Index(fields=['price'], name='doctors_ser_price_df9117_idx')],
            },
        ),
    ]
