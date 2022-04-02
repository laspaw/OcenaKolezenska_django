from django.shortcuts import render
from django.http import HttpResponse
from .models import Class
from .forms import ContactForm


# Create your views here.

def list_classes(request):
    context = {'classes_list': Class.objects.all()}
    return render(request, "teacher/list_classes.html", context)


def add_class(request):
    data = dict(email="lalala", title="Django", content="Forms", send_to_me="X")
    form = ContactForm(data)
    return render(request, "teacher/add_class.html", {"form": form.as_p()})


def show_class(request, class_id):
    myclass = Class.objects.get(pk=class_id)

    context = {
        'class_number': myclass.class_number,
        'class_letter': myclass.class_letter,
        'description': myclass.description,
        'school': myclass.school,
    }
    return render(request, "teacher/class_details.html", context)
