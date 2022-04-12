from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Class, Semester
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
    debug = ''
    form = AddStudentsForm()
    if request.method == "POST":
        debug = request.POST['students']
        if 'save' in request.POST:
            return redirect('teacher:show_class', class_id=class_id)
    return render(request, "teacher/add_students.html", {"form": form, 'debug': debug})


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
