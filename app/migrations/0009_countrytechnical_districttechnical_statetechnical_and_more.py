# Generated by Django 5.0.2 on 2024-03-02 22:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_appointment'),
    ]

    operations = [
        migrations.CreateModel(
            name='CountryTechnical',
            fields=[
                ('country', models.CharField(blank=True, max_length=155, primary_key=True, serialize=False)),
                ('technical_ref', models.ForeignKey(limit_choices_to={'user_type': 'technical'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DistrictTechnical',
            fields=[
                ('state', models.CharField(blank=True, max_length=155)),
                ('district', models.CharField(blank=True, max_length=155, primary_key=True, serialize=False)),
                ('technical_ref', models.ForeignKey(limit_choices_to={'user_type': 'technical'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StateTechnical',
            fields=[
                ('country', models.CharField(blank=True, max_length=155)),
                ('state', models.CharField(blank=True, max_length=155, primary_key=True, serialize=False)),
                ('technical_ref', models.ForeignKey(limit_choices_to={'user_type': 'technical'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TechnicalStaff',
            fields=[
                ('state', models.CharField(blank=True, max_length=155)),
                ('district', models.CharField(blank=True, max_length=155)),
                ('area', models.CharField(blank=True, max_length=155, primary_key=True, serialize=False)),
                ('technical_ref', models.ForeignKey(limit_choices_to={'user_type': 'technical'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
