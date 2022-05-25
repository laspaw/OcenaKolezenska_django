# Generated by Django 4.0.3 on 2022-03-28 12:13

import colorfield.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_number', models.IntegerField()),
                ('class_letter', models.CharField(max_length=1)),
                ('description', models.TextField()),
                ('school', models.CharField(max_length=64, null=True)),
                ('created_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='class2created_from', to='teacher.class')),
            ],
        ),
        migrations.CreateModel(
            name='Gradescale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=128, unique=True)),
                ('caption', models.CharField(max_length=64)),
                ('phone', models.CharField(blank=True, max_length=16, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=32)),
                ('classid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student2class', to='teacher.class')),
            ],
        ),
        migrations.CreateModel(
            name='Questionnaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ext_description', models.TextField(null=True)),
                ('deadline', models.DateTimeField(null=True)),
                ('is_stats_processed', models.BooleanField(default=True)),
                ('classid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questionnaire2class', to='teacher.class')),
                ('gradescale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questionnaire2gradescale', to='teacher.gradescale')),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=32)),
                ('svg_icon', models.CharField(max_length=128, null=True)),
                ('txt_color', colorfield.fields.ColorField(default='#000000', image_field=None, max_length=18, samples=None)),
                ('bg_color', colorfield.fields.ColorField(default='#FFFFFF', image_field=None, max_length=18, samples=None)),
                ('gradescale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grade2gradescale', to='teacher.gradescale')),
            ],
        ),
        migrations.AddField(
            model_name='class',
            name='semester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='class2semester', to='teacher.semester'),
        ),
        migrations.AddField(
            model_name='class',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='class2teacher', to='teacher.teacher'),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_timestamp', models.DateTimeField(auto_now_add=True)),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grade_id', to='teacher.grade')),
                ('graded_student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer2graded_student', to='teacher.student')),
                ('grading_student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer2grading_student', to='teacher.student')),
            ],
        ),
    ]