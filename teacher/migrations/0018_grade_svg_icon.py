# Generated by Django 4.0.3 on 2022-05-21 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0017_remove_grade_svg_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='grade',
            name='svg_icon',
            field=models.TextField(null=True),
        ),
    ]
