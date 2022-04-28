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
        classobj = Class.objects.create(**data)
        return redirect('teacher:add_students', class_id=classobj.id)
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


def add_questionnaire(request, class_id):
    questionnaire_id = 1
    if request.method == "POST":
        if 'save' in request.POST:
            return redirect('teacher:show_questionnaire', questionnaire_id=questionnaire_id)
        else:
            return redirect('teacher:show_class', class_id=class_id)
    else:
        form = AddQuestionnaireForm()
        return render(request, "teacher/add_questionnaire.html", {'form': form})


def show_questionnaire(request, questionnaire_id):
    return render(request, "teacher/show_questionnaire.html", {'questionnaire_id': questionnaire_id})

# def questionnaire(request, class_id):
#     my_questionnaire = Questionnaire.objects.get(pk=class_id)
#     context = {
#         'class_id': class_id,
#         'class_number': my_questionnaire.class_number,
#
#     }
#     return render(request, "teacher/show_class.html", context)
