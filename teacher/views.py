from .models import *
from .forms import *
from .icons import icons

import qrcode
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pendulum

import string
import random
import os
import io
import base64
import math

from django.shortcuts import render, redirect
from django.urls import resolve, reverse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist

matplotlib.use('Agg')  # puts tkinter used by matplotlib in web server mode
DIRS_TO_CREATE = ['static/qrcodes/']
for dir_to_create in DIRS_TO_CREATE:
    if not os.path.exists(dir_to_create):
        os.makedirs(dir_to_create)


def login(request):
    if request.method == "POST":
        form = AddClassForm(data=request.POST)
        data = {

        }
        if form.is_valid():
            pass
    else:
        form = AddClassForm()
    return render(request, "teacher/login.html", {"form": form} | icons)


def register(request):
    if request.method == "POST":
        form = AddClassForm(data=request.POST)
        data = {

        }
        if form.is_valid():
            pass
    else:
        form = AddClassForm()
    return render(request, "teacher/register.html", {"form": form} | icons)


def list_classes(request):
    context = {'classes_list': Class.objects.all()}
    return render(request, "teacher/list_classes.html", context | icons)


def delete_class(request, class_id):
    Class.objects.get(pk=class_id).delete()
    return redirect('teacher:list_classes')


def add_class(request):
    if request.method == "POST":
        form = AddClassForm(data=request.POST)
        if form.is_valid():
            data = {
                "class_number": request.POST['class_number'],
                "class_letter": request.POST['class_letter'].capitalize(),
                "school": request.POST['school'],
                "semester_id": Semester.get_current_semester().id,
                "teacher_id": 1,
            }
            class_obj = Class.objects.create(**data)
            return redirect('teacher:add_students', class_id=class_obj.id)
    else:
        form = AddClassForm()
    return render(request, "teacher/add_class.html", {"form": form} | icons)


def modify_class(request, class_id):
    try:
        class_obj = Class.objects.get(pk=class_id)
    except ObjectDoesNotExist:
        return render(request, "teacher/404.html")

    if request.method == "POST":
        form = AddClassForm(data=request.POST)
        if form.is_valid():
            class_obj.class_number = request.POST['class_number']
            class_obj.class_letter = request.POST['class_letter'].capitalize()
            class_obj.school = request.POST['school']
            class_obj.save()
            return redirect('teacher:modify_students', class_id=class_obj.id)
    elif request.method == "GET":
        form = AddClassForm(action='modify', initial={
            'class_number': class_obj.class_number,
            'class_letter': class_obj.class_letter,
            'school': class_obj.school,
        })
    return render(request, "teacher/add_class.html", {"form": form} | icons)


def add_students(request, class_id):
    review_students_list = ['po wprowadzeniu listy uczniów kliknij w <Sprawdź>',
                            'w tym oknie pojawi się lista uczniów',
                            'gdy lista będzie poprawna, kliknij <Zapisz>',
                            ]
    if request.method == "POST":
        form = AddStudentsForm(data=request.POST)
        review_students_text = request.POST['students']
        review_students_list = Student.cleanup_and_convert_review_students_text_to_list(
            review_students_text, request.POST.get('mask_lastnames', False))
        if 'save' in request.POST:
            for student in review_students_list:
                data = {
                    'name': student,
                    'personal_questionnaire_id': 'qID' + ''.join(random.choices(string.ascii_letters + string.digits, k=20)),
                    'classid_id': class_id,
                }
                Student.objects.create(**data)
            return redirect('teacher:show_class', class_id=class_id)
    elif request.method == "GET":
        form = AddStudentsForm()
    return render(request, "teacher/add_students.html", {'form': form, 'review_students_list': review_students_list} | icons)


def modify_students(request, class_id):
    review_students_list = []
    if request.method == "POST":
        form = AddStudentsForm(data=request.POST)
        review_students_text = request.POST['students']
        review_students_list = Student.cleanup_and_convert_review_students_text_to_list(
            review_students_text, request.POST.get('mask_lastnames', False))
        if 'save' in request.POST:
            if form.is_valid():
                Student.objects.filter(classid_id=class_id).delete()
                for student in review_students_list:
                    data = {
                        'name': student,
                        'personal_questionnaire_id': 'qID' + ''.join(random.choices(string.ascii_letters + string.digits, k=20)),
                        'classid_id': class_id,
                    }
                    Student.objects.create(**data)
            return redirect('teacher:show_class', class_id=class_id)
    if request.method == "GET":
        form = AddStudentsForm(initial={'students': Student.get_students_list_for_modify(class_id)})
    return render(request, "teacher/add_students.html", {'form': form, 'review_students_list': review_students_list} | icons)


def delete_questionnaire(request, questionnaire_id):
    my_questionnaire = Questionnaire.objects.get(pk=questionnaire_id)
    class_id = Class.objects.get(pk=my_questionnaire.classid_id).id
    my_questionnaire.delete()
    return redirect('teacher:show_class', class_id=class_id)


def show_class(request, class_id):
    my_class = Class.objects.get(pk=class_id)
    students = Student.objects.filter(classid_id=class_id)
    students = [student.name for student in students]
    context = {
        'my_class': my_class,
        'students': students,
    }
    return render(request, "teacher/show_class.html", context | icons)


def open_close_questionnaire(request, questionnaire_id):
    my_questionnaire = Questionnaire.objects.get(pk=questionnaire_id)
    if my_questionnaire.is_closed:
        my_questionnaire.is_closed = False
    else:
        my_questionnaire.is_closed = True
    my_questionnaire.save()
    return redirect('teacher:show_questionnaire', questionnaire_id=questionnaire_id)


def add_questionnaire(request, class_id, action):
    if action not in ['add', 'modify', ]:
        return render(request, "teacher/409_bad_action.html", {'action': action} | icons)
    questionnaire_qs = Questionnaire.objects.filter(classid_id=class_id)

    if len(questionnaire_qs) == 0:  # nie ma ankiety -> utwórz ją
        if request.method == "POST":
            if 'save' in request.POST:
                data = {
                    'deadline': Questionnaire.clear_deadline(request.POST['deadline']),
                    'message_to_students': request.POST['message_to_students'],
                    'gradescale_id': request.POST['gradescale'],
                    'classid_id': class_id
                }
                questionnaire_obj = Questionnaire.objects.create(**data)
                return redirect('teacher:show_questionnaire', questionnaire_id=questionnaire_obj.id)
            elif 'return' in request.POST:
                return redirect('teacher:show_class', class_id=class_id)
        elif request.method == "GET":
            form = AddQuestionnaireForm(action=action)
            return render(request, "teacher/add_questionnaire.html", {'form': form} | icons)

    if len(questionnaire_qs) == 1:  # ankieta istnieje -> wyświetl lub modyfikuj
        questionnaire_obj = questionnaire_qs[0]
        if request.method == "POST":
            questionnaire_obj.deadline = Questionnaire.clear_deadline(request.POST['deadline'])
            questionnaire_obj.message_to_students = request.POST['message_to_students']
            questionnaire_obj.gradescale_id = request.POST['gradescale']
            questionnaire_obj.save()
            return redirect('teacher:show_questionnaire', questionnaire_id=questionnaire_obj.id)
        elif request.method == "GET":
            if action == 'add':
                return redirect('teacher:show_questionnaire', questionnaire_id=questionnaire_obj.id)
            elif action == 'modify':
                form = AddQuestionnaireForm(action=action, initial={
                    'deadline': questionnaire_obj.deadline,
                    'message_to_students': questionnaire_obj.message_to_students,
                    'gradescale_id': questionnaire_obj.gradescale_id,
                })
                return render(request, "teacher/add_questionnaire.html", {'form': form} | icons)


def show_questionnaire(request, questionnaire_id):
    questionnaire_obj = Questionnaire.objects.get(pk=questionnaire_id)
    my_class = Class.objects.get(pk=questionnaire_obj.classid_id)
    students = Student.objects.filter(classid=questionnaire_obj.classid_id)
    for student in students:
        url = request.build_absolute_uri(reverse('teacher:personal_questionnaire', args=(student.personal_questionnaire_id,)))
        student.absolute_questionnaire_url = url
        student.qrcode_path = f'qrcodes/{student.personal_questionnaire_id}.png'
        img = qrcode.make(url)
        img.save('static/' + student.qrcode_path)

    context = {
        'my_class': my_class,
        'questionnaire_id': questionnaire_id,
        'deadline': Questionnaire.get_deadline_caption(questionnaire_obj.deadline),
        'is_closed': questionnaire_obj.is_closed,
        'is_overdue': Questionnaire.check_overdue(questionnaire_obj.deadline),
        'message_to_students': questionnaire_obj.message_to_students.split('\n') if len(questionnaire_obj.message_to_students) > 0 else None,
        'gradescale': questionnaire_obj.gradescale.caption,
        'students': students,
    }
    return render(request, "teacher/show_questionnaire.html", context | icons)


def personal_questionnaire(request, personal_questionnaire_id):
    student_obj = Student.objects.filter(personal_questionnaire_id=personal_questionnaire_id)
    if not student_obj:
        return render(request, "teacher/404.html")
    student_obj = student_obj[0]
    class_obj = student_obj.classid
    questionnaire_obj = class_obj.questionnaire2class.last()
    gradescale_obj = questionnaire_obj.gradescale
    grades = gradescale_obj.grade2gradescale.all()

    # clear request.POST from keys related with saved grades
    GRADES_PREFIX = 'studentid'
    answers_dict = {}
    for request_POST_key, request_POST_value in request.POST.items():
        if request_POST_key.startswith(GRADES_PREFIX):
            answers_dict[request_POST_key] = request_POST_value

    # save answers to database
    if request.method == "POST":
        counter = 0
        for answer_key, answer_value in answers_dict.items():
            counter += 1
            studentid = answer_key[len(GRADES_PREFIX):]
            if answer := Answer.objects.filter(grading_student=student_obj.id, graded_student=studentid):
                answer.update(
                    grading_student_id=student_obj.id,
                    graded_student_id=studentid,
                    grade_id=int(answer_value),
                )
            else:
                Answer.objects.create(
                    grading_student_id=student_obj.id,
                    graded_student_id=studentid,
                    grade_id=int(answer_value),
                )
        student_obj.questionnaire_response_rate = int(counter / class_obj.student2class.count() * 100)
        student_obj.save()

    # load answers from database to be checked in form
    for answer in Answer.objects.filter(grading_student=student_obj.id):
        answers_dict[GRADES_PREFIX + str(answer.graded_student.id)] = answer.grade.id

    form = PersonalQuestionnaireForm(
        answers=answers_dict,
        grades_prefix=GRADES_PREFIX,
        class_obj=class_obj,
        grades=grades,
        is_overdue=Questionnaire.check_overdue(questionnaire_obj.deadline),
    )

    context = {
        'student_name': student_obj.name,
        'deadline': Questionnaire.get_deadline_caption(questionnaire_obj.deadline),
        'is_overdue': Questionnaire.check_overdue(questionnaire_obj.deadline),
        'is_closed': questionnaire_obj.is_closed,
        'message_to_students': questionnaire_obj.message_to_students.split('\n'),
        'form': form,
    }
    return render(request, "teacher/personal_questionnaire.html", context | icons)


class Statistics(View):
    student_obj = None
    my_class_obj = None
    questionnaire_obj = None
    gradescale_obj = None

    def get_all_grades_attr(self, attr_name):
        return [grade.__getattribute__(attr_name) for grade in Grade.objects.filter(gradescale_id=self.gradescale_obj.id)]

    @staticmethod
    def extract_attr_list_from_obj_list(obj_list, attr_name):
        return [obj.__getattribute__(attr_name) for obj in obj_list]

    def collect_grade_sum_matrix(self):
        colleagues_id = self.extract_attr_list_from_obj_list(Student.objects.filter(classid_id=self.my_class_obj.id), 'id')
        grade_sum_matrix = np.zeros((len(self.get_all_grades_attr('id')), len(colleagues_id)), dtype=int)
        grade_index = 0
        for grade_id in self.get_all_grades_attr('id'):
            colleague_index = 0
            for colleague_id in colleagues_id:
                grade_sum_matrix[grade_index][colleague_index] = Answer.objects.filter(graded_student_id=colleague_id, grade_id=grade_id).count()
                colleague_index += 1
            grade_index += 1
        return grade_sum_matrix

    def collect_self_grade_matrix(self):
        self_grade_matrix = [0]
        colleagues_id = self.extract_attr_list_from_obj_list(Student.objects.filter(classid_id=self.my_class_obj.id), 'id')
        for colleague_id in colleagues_id:
            self_answer = Answer.objects.filter(grading_student_id=colleague_id, graded_student_id=colleague_id).first()
            if self_answer:
                self_grade_matrix.append(self_answer.grade.int_value)
        return self_grade_matrix

    def create_plot(self, y_grades, mean_grades, title='', xlabel='', ylabel='liczba ocen', plot_label='średnia klasowa'):
        # set predefined attributes
        font_large = {'family': 'Helvetica', 'color': 'black', 'size': 16}
        font_regular = {'family': 'Helvetica', 'color': 'black', 'size': 12}

        # add "pad" to zero values
        y_grades = [0.01 if y_grade == 0 else y_grade for y_grade in y_grades]

        # configure plots
        plt.axes().set_facecolor('#ffffff00')
        fig = plt.figure(facecolor='#ffffff00', figsize=(10, 5))
        plt.title(title, fontdict=font_large)
        plt.xlabel(xlabel, fontdict=font_regular)
        plt.ylabel(ylabel, fontdict=font_regular)
        plt.grid(axis='y', color='blue', linestyle=':', linewidth=0.25)
        plt.bar(self.get_all_grades_attr('caption'), y_grades, width=0.5, color=self.get_all_grades_attr('bg_color'))
        plt.plot(self.get_all_grades_attr('caption'), mean_grades, color='blue', label=plot_label)
        plt.legend()
        plt.xticks(rotation=10)
        plt.yticks(range(0, math.ceil(max(y_grades + mean_grades)) + 1))

        # save to memory
        img_in_memory = io.BytesIO()
        fig.tight_layout()
        plt.savefig(img_in_memory, format="png")
        plt.close(fig)
        img_in_memory = base64.b64encode(img_in_memory.getvalue()).decode('utf8')
        return img_in_memory

    def get(self, request, student_id):
        self.student_obj = Student.objects.get(pk=student_id)
        self.my_class_obj = Class.objects.get(pk=self.student_obj.classid_id)
        self.questionnaire_obj = self.my_class_obj.questionnaire2class.first()
        self.gradescale_obj = self.questionnaire_obj.gradescale
        grades = self.gradescale_obj.grade2gradescale.all()

        # collect general data
        class_mean_grades_matrix = [np.mean(answers_sum) for answers_sum in self.collect_grade_sum_matrix()]
        students_in_class = Student.objects.filter(classid_id=self.my_class_obj.id).count() - 1

        # collect self grade data
        self_grade = Answer.objects.filter(grading_student_id=student_id, graded_student_id=student_id).first()
        self_grade_mean = np.round(np.mean(self.collect_self_grade_matrix()), 1)
        self_grade_median = np.round(np.median(self.collect_self_grade_matrix()), 1)

        # collect collected grades data
        student_collected_answers = Answer.objects.filter(graded_student_id=self.student_obj.id).exclude(grading_student_id=self.student_obj.id)
        student_collected_grades_list = [answer.grade.int_value for answer in student_collected_answers]
        student_collected_grades_counts_matrix = [student_collected_grades_list.count(grade) for grade in self.get_all_grades_attr('int_value')]
        student_collected_grades_plot = self.create_plot(student_collected_grades_counts_matrix, class_mean_grades_matrix)  # plot as svg_icon in memory

        student_collected_grades_sum = len(student_collected_grades_list)
        if students_in_class > 0:
            student_collected_grades_percent = np.round(student_collected_grades_sum / students_in_class * 100, 1)
        else:
            student_collected_grades_percent = -1
        student_mean_collected_grade = 0 if np.isnan(ret := np.round(np.mean(student_collected_grades_list), 1)) else ret
        student_median_collected_grade = 0 if np.isnan(ret := np.round(np.median(student_collected_grades_list), 1)) else ret
        grading_students_names = {}
        for grade in Grade.objects.filter(gradescale_id=self.gradescale_obj.id):
            grading_students_names[grade] = [answer.grading_student.name for answer in student_collected_answers.filter(grade_id=grade.id)]

        # collect given grades data
        student_given_answers = Answer.objects.filter(grading_student_id=self.student_obj.id).exclude(graded_student_id=self.student_obj.id)
        student_given_grades_list = [answer.grade.int_value for answer in student_given_answers]
        student_given_grades_counts_matrix = [student_given_grades_list.count(grade) for grade in self.get_all_grades_attr('int_value')]
        student_given_grades_plot = self.create_plot(student_given_grades_counts_matrix, class_mean_grades_matrix)  # plot as svg_icon in memory

        student_given_grades_sum = len(student_given_grades_list)
        if students_in_class > 0:
            student_given_grades_percent = np.round(student_given_grades_sum / students_in_class * 100, 1)
        else:
            student_given_grades_percent = -1
        student_mean_given_grade = 0 if np.isnan(ret := np.round(np.mean(student_given_grades_list), 1)) else ret
        student_median_given_grade = 0 if np.isnan(ret := np.round(np.median(student_given_grades_list), 1)) else ret
        graded_students_names = {}
        for grade in Grade.objects.filter(gradescale_id=self.gradescale_obj.id):
            graded_students_names[grade] = [answer.graded_student.name for answer in student_given_answers.filter(grade_id=grade.id)]

        context = {
            'debug': 'grading_students_names',

            # general data
            'student_obj': self.student_obj,
            'my_class': self.my_class_obj,
            'students_in_class': students_in_class,

            # self grade data
            'styles': PersonalQuestionnaireForm.render_styles(grades),
            'grades': grades,
            'self_grade': self_grade,
            'self_grade_mean': self_grade_mean,
            'self_grade_median': self_grade_median,

            # collected grades data
            'student_collected_grades_sum': student_collected_grades_sum,
            'student_collected_grades_percent': student_collected_grades_percent,
            'student_mean_collected_grade': student_mean_collected_grade,
            'student_median_collected_grade': student_median_collected_grade,
            'student_collected_grades_plot': student_collected_grades_plot,
            'grading_students_names': grading_students_names,

            # given grades data
            'student_given_grades_sum': student_given_grades_sum,
            'student_given_grades_percent': student_given_grades_percent,
            'student_mean_given_grade': student_mean_given_grade,
            'student_median_given_grade': student_median_given_grade,
            'student_given_grades_plot': student_given_grades_plot,
            'graded_students_names': graded_students_names,

        }
        return render(request, "teacher/statistics.html", context | icons)
