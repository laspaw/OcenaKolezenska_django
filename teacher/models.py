from django.db import models
from colorfield.fields import ColorField
import pendulum


class Semester(models.Model):
    name = models.CharField(max_length=16)

    @staticmethod
    def get_semester_caption(date: pendulum.datetime) -> str:
        first_semester_start_month = 9
        second_semester_start_month = 3
        school_semester = 'I'
        if date.month >= first_semester_start_month:
            school_year = str(date.year) + '/' + str("%02d" % ((date.year + 1) % 100))
        else:
            school_year = str(date.year - 1) + '/' + str("%02d" % (date.year % 100))
            if date.month >= second_semester_start_month:
                school_semester = 'II'
        return school_year + " " + school_semester


class Teacher(models.Model):
    email = models.EmailField(max_length=128, unique=True)
    name = models.CharField(max_length=64)
    phone = models.CharField(max_length=16, null=True, blank=True, unique=True)


class Class(models.Model):
    class_number = models.IntegerField()
    class_letter = models.CharField(max_length=1)
    school = models.CharField(max_length=64, null=True)
    semester = models.ForeignKey('Semester', on_delete=models.CASCADE, related_name='class2semester')
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, related_name='class2teacher')
    created_from = models.ForeignKey('Class', on_delete=models.CASCADE, related_name='class2created_from', null=True)

    def __str__(self):
        return str(self.class_number) + self.class_letter + " (" + self.school + ")"


class Questionnaire(models.Model):
    ext_description = models.TextField(null=True)
    deadline = models.DateTimeField(null=True)
    is_stats_processed = models.BooleanField(default=True)
    gradescale = models.ForeignKey("Gradescale", on_delete=models.CASCADE, related_name='questionnaire2gradescale')
    classid = models.ForeignKey("Class", on_delete=models.CASCADE, related_name='questionnaire2class')


class Student(models.Model):
    name = models.CharField(max_length=32)
    classid = models.ForeignKey("Class", on_delete=models.CASCADE, related_name='student2class')


class Answer(models.Model):
    answer_timestamp = models.DateTimeField(auto_now_add=True)
    grading_student = models.ForeignKey("Student", on_delete=models.CASCADE, related_name='answer2grading_student')
    graded_student = models.ForeignKey("Student", on_delete=models.CASCADE, related_name='answer2graded_student')
    grade = models.ForeignKey("Grade", on_delete=models.CASCADE, related_name='grade_id')


class Grade(models.Model):
    caption = models.CharField(max_length=32)
    int_value = models.IntegerField()
    image = models.CharField(max_length=128, null=True)
    txt_color = ColorField(default='#000000', null=True)
    bg_color = ColorField(default='#FFFFFF', null=True)
    gradescale = models.ForeignKey("Gradescale", on_delete=models.CASCADE, related_name='grade2gradescale')


class Gradescale(models.Model):
    caption = models.CharField(max_length=32)


# abstract class timestaped:
#     created_at = models.DateTimeField(auto_now_add=True)
#     modified_at = models.DateTimeField(auto_now=True)
#     is_active = models.BooleanField(default=True)
#     deactivated_at = models.DateTimeField(null=True)
#     is_deleted = models.BooleanField(default=False)
#     deleted_at = models.DateTimeField(null=True)
