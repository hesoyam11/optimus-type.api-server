# Generated by Django 3.0.7 on 2020-06-19 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0002_attempt'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='attempt_counter',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
