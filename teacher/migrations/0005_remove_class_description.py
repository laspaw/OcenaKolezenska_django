# Generated by Django 4.0.3 on 2022-04-04 14:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0004_alter_class_created_from'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='class',
            name='description',
        ),
    ]