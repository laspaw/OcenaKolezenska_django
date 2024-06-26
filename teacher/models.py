import pendulum
from django.db import models
from colorfield.fields import ColorField


class Semester(models.Model):
    caption = models.CharField(max_length=16)

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
    def get_current_semester():
        current_semester_caption = Semester.get_semester_caption(pendulum.now())
        if current_semester := Semester.objects.filter(caption=current_semester_caption).first():
            return current_semester
        return Semester.objects.create(caption=current_semester_caption)

    def __str__(self):
        return str(self.caption)


class Teacher(models.Model):
    email = models.EmailField(max_length=128, unique=True)
    name = models.CharField(max_length=64)
    phone = models.CharField(max_length=16, null=True, blank=True, unique=True)

    def __str__(self):
        return str(self.name)


class Class(models.Model):
    class_number = models.IntegerField()
    class_letter = models.CharField(max_length=1)
    school = models.CharField(max_length=128, null=True)
    semester = models.ForeignKey('Semester', on_delete=models.CASCADE, related_name='class2semester')
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, related_name='class2teacher')
    created_from = models.ForeignKey('Class', on_delete=models.CASCADE, related_name='class2created_from', null=True)

    def __str__(self):
        return str(self.class_number) + str(self.class_letter) + (" (" + self.school + ")" if len(self.school) > 0 else '')


class Questionnaire(models.Model):
    deadline = models.DateTimeField(null=True)
    message_to_students = models.TextField(null=True)
    is_stats_processed = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    gradescale = models.ForeignKey("Gradescale", on_delete=models.CASCADE, related_name='questionnaire2gradescale')
    classid = models.ForeignKey("Class", on_delete=models.CASCADE, unique=True, related_name='questionnaire2class')

    def __str__(self):
        return 'Questionnaire for class_id=' + str(self.classid)

    @staticmethod
    def get_deadline_caption(deadline):
        if deadline is None:
            return None
        now = pendulum.now()
        deadline = pendulum.instance(deadline)
        return f"{deadline.in_timezone(now.timezone).strftime('%Y-%m-%d %H:%M')} {now.tzname()}"

    @staticmethod
    def check_overdue(deadline):
        if deadline is None:
            return False
        return pendulum.now() > deadline

    @staticmethod
    def clear_deadline(deadline):
        if deadline == '' or pendulum.now() > pendulum.instance(pendulum.parse(deadline)):
            return None
        else:
            return deadline


class Student(models.Model):
    name = models.CharField(max_length=32)
    classid = models.ForeignKey("Class", on_delete=models.CASCADE, related_name='student2class')
    personal_questionnaire_id = models.CharField(max_length=128, null=True, unique=True)
    questionnaire_response_rate = models.IntegerField(default=0)
    absolute_questionnaire_url = ''
    qrcode_path = ''

    @staticmethod
    def cleanup_and_convert_review_students_text_to_list(review_students_text: str, mask_last_name: bool):
        review_students_list = review_students_text.split('\n')
        return_list = []
        for list_item in review_students_list:
            temp = list_item.strip().split(' ')
            if len(temp) < 2:
                continue
            if mask_last_name:
                temp[0] = temp[0][:1] + '*' * (len(temp[0]) - 1)
            return_list.append(temp[1] + ' ' + temp[0])
        return return_list

    @staticmethod
    def get_students_list_for_modify(class_id):
        return_list = ''
        for student in Student.objects.filter(classid_id=class_id):
            first_name, last_name = student.name.split(' ')
            return_list += last_name + ' ' + first_name + '\n'
        return return_list

    def __str__(self):
        return str(self.name)


class Answer(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['grading_student', 'graded_student'], name='unique grading to graded')
        ]

    answer_timestamp = models.DateTimeField(auto_now_add=True)
    grading_student = models.ForeignKey("Student", on_delete=models.CASCADE, related_name='answer2grading_student')
    graded_student = models.ForeignKey("Student", on_delete=models.CASCADE, related_name='answer2graded_student')
    grade = models.ForeignKey("Grade", on_delete=models.CASCADE, related_name='answer2grade')

    def __str__(self):
        return f'grade {self.grade} from {self.grading_student} to {self.graded_student}'


class Grade(models.Model):
    caption = models.CharField(max_length=32)
    int_value = models.IntegerField()
    svg_icon = models.TextField(null=True)
    bg_color = ColorField(default='#888888')
    gradescale = models.ForeignKey("Gradescale", on_delete=models.CASCADE, related_name='grade2gradescale')

    def __str__(self):
        return str(self.caption)


class Gradescale(models.Model):
    caption = models.CharField(max_length=64)

    def __str__(self):
        return str(self.caption)

# abstract class timestaped:
#     created_at = models.DateTimeField(auto_now_add=True)
#     modified_at = models.DateTimeField(auto_now=True)
#     is_active = models.BooleanField(default=True)
#     deactivated_at = models.DateTimeField(null=True)
#     is_deleted = models.BooleanField(default=False)
#     deleted_at = models.DateTimeField(null=True)
