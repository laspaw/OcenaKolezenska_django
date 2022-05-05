"""OcenaKolezenska URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

app_name = "teacher"
urlpatterns = [
                  path('show_class/<int:class_id>', show_class, name="show_class"),
                  path('add_class/', add_class, name="add_class"),
                  path('add_students/<int:class_id>', add_students, name="add_students"),
                  path('delete_class/<int:class_id>', delete_class, name="delete_class"),
                  path('', list_classes, name="list_classes"),
                  path('add_questionnaire/<int:class_id>', add_questionnaire, name="add_questionnaire"),
                  path('show_questionnaire/<int:questionnaire_id>', show_questionnaire, name="show_questionnaire"),
                  path('delete_questionnaire/<int:questionnaire_id>', delete_questionnaire, name="delete_questionnaire"),
                  path('questionnaire/<peronal_questionnaire_id>', peronal_questionnaire, name="peronal_questionnaire"),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
