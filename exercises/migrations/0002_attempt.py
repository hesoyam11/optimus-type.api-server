# Generated by Django 3.0.6 on 2020-06-06 06:34

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('exercises', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attempt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('layout', models.CharField(choices=[('enUSAQ', 'en_US.Am.QWERTY'), ('enUSAD', 'en_US.Am.Dvorak'), ('enUSAC', 'en_US.Am.Colemak'), ('ukUAAЙ', 'uk_UA.Am.ЙЦУКЕН'), ('ruRUAЙ', 'ru_RU.Am.ЙЦУКЕН')], max_length=6)),
                ('input_time_logs', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(), size=4096)),
                ('time_spent', models.PositiveIntegerField()),
                ('mistake_time_logs', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(), size=32)),
                ('mistake_char_logs', models.CharField(max_length=32)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attempts', to=settings.AUTH_USER_MODEL)),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attempts', to='exercises.Exercise')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
    ]
