# Generated by Django 4.0.3 on 2022-05-26 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionnaire',
            name='is_closed',
            field=models.BooleanField(default=False),
        ),
    ]
