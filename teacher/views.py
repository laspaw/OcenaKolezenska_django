from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Class, Semester
from .forms import AddClassForm


# Create your views here.

def list_classes(request):
    context = {'classes_list': Class.objects.all()}
    return render(request, "teacher/list_classes.html", context)


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
        #        return render(request, f"teacher/class_details.html/{classobj.id}")
        return redirect('teacher:show_class', class_id=classobj.id)
    else:
        form = AddClassForm()
        return render(request, "teacher/add_class.html", {"form": form})


def delete_class(request, class_id):
    Class.objects.get(pk=class_id).delete()
    return redirect('teacher:list_classes')


def show_class(request, class_id):
    myclass = Class.objects.get(pk=class_id)

    context = {
        'class_id': class_id,
        'class_number': myclass.class_number,
        'class_letter': myclass.class_letter,
        'semester': myclass.semester.name,
        'school': myclass.school,
    }
    return render(request, "teacher/class_details.html", context)
