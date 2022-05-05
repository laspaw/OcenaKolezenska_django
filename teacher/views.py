import string
import random
from django.shortcuts import render, redirect
from .models import *
from .forms import *


def list_classes(request):
    context = {'classes_list': Class.objects.all()}
    return render(request, "teacher/list_classes.html", context)


def delete_class(request, class_id):
    Class.objects.get(pk=class_id).delete()
    return redirect('teacher:list_classes')


def add_class(request):
    if request.method == "POST":
        data = {
            "class_number": request.POST['class_number'],
            "class_letter": request.POST['class_letter'],
            "school": request.POST['school'],
            "semester_id": request.POST['semester'],
            "teacher_id": 1,
        }
        class_obj = Class.objects.create(**data)
        return redirect('teacher:add_students', class_id=class_obj.id)
    form = AddClassForm()
    return render(request, "teacher/add_class.html", {"form": form})


def show_class(request, class_id):
    my_class = Class.objects.get(pk=class_id)
    students_queryset = Student.objects.filter(classid_id=class_id)
    students = [student.name for student in students_queryset]
    context = {
        'class_id': class_id,
        'class_number': my_class.class_number,
        'class_letter': my_class.class_letter,
        'semester': my_class.semester.name,
        'school': my_class.school,
        'students': students,
    }
    return render(request, "teacher/show_class.html", context)


def add_students(request, class_id):
    review_students_list = ['po wprowadzeniu listy uczniów kliknij w <Sprawdź>',
                            'w tym oknie pojawi się lista uczniów',
                            'kiedy ta lista będzie poprawna, kliknij w<Zapisz>',
                            ]
    if request.method == "POST":
        form = AddStudentsForm(data=request.POST)
        review_students_text = request.POST['students']
        review_students_list = Student.cleanup_and_convert_review_students_text_to_list(
            review_students_text, request.POST.get('mask_lastnames', False))
        if 'save' in request.POST:
            for student in review_students_list:
                Student.objects.create(name=student, classid_id=class_id)
            return redirect('teacher:show_class', class_id=class_id)
    else:
        form = AddStudentsForm()
    return render(request, "teacher/add_students.html", {'form': form, 'review_students_list': review_students_list})


def delete_questionnaire(request, questionnaire_id):
    my_questionnaire = Questionnaire.objects.get(pk=questionnaire_id)
    class_id = Class.objects.get(pk=my_questionnaire.classid_id).id
    my_questionnaire.delete()
    return redirect('teacher:show_class', class_id=class_id)


def add_questionnaire(request, class_id):
    questionnaire_id = Questionnaire.objects.filter(classid_id=class_id)
    if len(questionnaire_id) == 0:
        if request.method == "POST":
            if 'save' in request.POST:
                deadline = request.POST['deadline']
                if deadline == '':
                    deadline = None
                print(deadline)
                print(type(deadline))
                data = {
                    'deadline': deadline,
                    'message_to_students': request.POST['message_to_students'],
                    'gradescale_id': request.POST['gradescale'],
                    'classid_id': class_id
                }
                questionnaire_obj = Questionnaire.objects.create(**data)
                for student in Student.objects.filter(classid_id=class_id):
                    student.personal_questionnaire_link = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
                    student.save()
                return redirect('teacher:show_questionnaire', questionnaire_id=questionnaire_obj.id)
            elif 'return' in request.POST:
                return redirect('teacher:show_class', class_id=class_id)
        elif request.method == "GET":
            form = AddQuestionnaireForm()
            return render(request, "teacher/add_questionnaire.html",
                          {'form': form, 'class_name': Class.objects.get(pk=class_id)})
    if len(questionnaire_id) == 1:
        return redirect('teacher:show_questionnaire', questionnaire_id=questionnaire_id[0].id)


def show_questionnaire(request, questionnaire_id):
    my_questionnaire = Questionnaire.objects.get(pk=questionnaire_id)
    class_name = Class.objects.get(pk=my_questionnaire.classid_id)
    students = Student.objects.filter(classid=my_questionnaire.classid_id)
    # - wyśietlanie linków dla uczniów + QRcode

    context = {
        'class_name': class_name,
        'questionnaire_id': questionnaire_id,
        'deadline': None if my_questionnaire.deadline is None else my_questionnaire.deadline.strftime('%Y-%d-%m %H:%M'),
        'message_to_students': my_questionnaire.message_to_students.split('\n'),
        'gradescale': my_questionnaire.gradescale.caption,
        'students': students,
    }
    return render(request, "teacher/show_questionnaire.html", context)


def peronal_questionnaire(request, peronal_questionnaire_id):
    jeżeli jest ankieta ->

    Student.objects.filter(personal_questionnaire_link=peronal_questionnaire_id)

    my_questionnaire = Questionnaire.objects.get(pk=questionnaire_id)
    class_name = Class.objects.get(pk=my_questionnaire.classid_id)
    students = Student.objects.filter(classid=my_questionnaire.classid_id)
    # - wyśietlanie linków dla uczniów + QRcode

    context = {
        'class_name': class_name,
        'questionnaire_id': questionnaire_id,
        'deadline': None if my_questionnaire.deadline is None else my_questionnaire.deadline.strftime('%Y-%d-%m %H:%M'),
        'message_to_students': my_questionnaire.message_to_students.split('\n'),
        'gradescale': my_questionnaire.gradescale.caption,
        'students': students,
    }
    return render(request, "teacher/show_questionnaire.html", context)



