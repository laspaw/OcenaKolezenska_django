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

    @staticmethod
    def get_semester_choices():
        temp_list1 = []
        temp_list2 = []
        semesters = Semester.objects.all()[:20]
        for semester in semesters:
            if semester.name == Semester.get_semester_caption(pendulum.now()):
                temp_list1 = [(semester.id, 'bieżący ' + semester.name)]
            temp_list2.append((semester.id, semester.name))
        return tuple(temp_list1 + temp_list2)


class Teacher(models.Model):
    email = models.EmailField(max_length=128, unique=True)
    name = models.CharField(max_length=64)
    phone = models.CharField(max_length=16, null=True, blank=True, unique=True)


class Class(models.Model):
    class_number = models.IntegerField()
    class_letter = models.CharField(max_length=1)
    school = models.CharField(max_length=128, null=True)
    semester = models.ForeignKey('Semester', on_delete=models.CASCADE, related_name='class2semester')
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, related_name='class2teacher')
    created_from = models.ForeignKey('Class', on_delete=models.CASCADE, related_name='class2created_from', null=True)

    def __str__(self):
        return str(self.class_number) + self.class_letter + (" (" + self.school + ")" if len(self.school) > 0 else '')


class Questionnaire(models.Model):
    deadline = models.DateTimeField(null=True)
    message_to_students = models.TextField(null=True)
    is_stats_processed = models.BooleanField(default=False)
    gradescale = models.ForeignKey("Gradescale", on_delete=models.CASCADE, related_name='questionnaire2gradescale')
    classid = models.ForeignKey("Class", on_delete=models.CASCADE, unique=True, related_name='questionnaire2class')


class Student(models.Model):
    name = models.CharField(max_length=32)
    classid = models.ForeignKey("Class", on_delete=models.CASCADE, related_name='student2class')
    personal_questionnaire_link = models.CharField(max_length=128, null=True, unique=True)

    @staticmethod
    def cleanup_and_convert_review_students_text_to_list(review_students_text: str, mask_last_name: bool):
        review_students_list = review_students_text.split('\n')
        return_list = []
        temp = None
        for list_item in review_students_list:
            temp = list_item.strip().split(' ')
            if len(temp) < 2:
                continue
            if mask_last_name:
                temp[0] = temp[0][:1] + '*' * (len(temp[0]) - 1)
            return_list.append(temp[1] + ' ' + temp[0])
        return return_list


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
    @staticmethod
    def get_gradescale_choices():
        return ((gradescale.id, gradescale.caption,) for gradescale in Gradescale.objects.all())

    caption = models.CharField(max_length=64)

# abstract class timestaped:
#     created_at = models.DateTimeField(auto_now_add=True)
#     modified_at = models.DateTimeField(auto_now=True)
#     is_active = models.BooleanField(default=True)
#     deactivated_at = models.DateTimeField(null=True)
#     is_deleted = models.BooleanField(default=False)
#     deleted_at = models.DateTimeField(null=True)
