# Generated by Django 5.0.2 on 2024-03-02 23:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_appointment_meet_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='doctor',
        ),
    ]