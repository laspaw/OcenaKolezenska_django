# Generated by Django 4.0.3 on 2022-05-21 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0015_alter_grade_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grade',
            name='svg_icon',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
