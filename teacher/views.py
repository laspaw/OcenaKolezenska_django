from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Class, Semester, Student
from .forms import *


# Create your views here.

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


def add_students(request, class_id):
    review_students_text = ''
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
            return redirect('teacher:show_class', class_id=class_id)
    else:
        form = AddStudentsForm()
    return render(request, "teacher/add_students.html", {"form": form, 'review_students_list': review_students_list})


def show_class(request, class_id):
    myclass = Class.objects.get(pk=class_id)

    context = {
        'class_id': class_id,
        'class_number': myclass.class_number,
        'class_letter': myclass.class_letter,
        'semester': myclass.semester.name,
        'school': myclass.school,
    }
    return render(request, "teacher/show_class.html", context)
