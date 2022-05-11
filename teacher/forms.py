from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, HTML, ButtonHolder, Row, Column
from django import forms
from .views import *
from .models import *


class AddClassForm(forms.Form):
    semester = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-select'}),
        choices=Semester.get_semester_choices(), label='wybierz semestr',
    )
    class_number = forms.CharField(
        max_length=1,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'np: 1'}),
        label='cyfra klasy:',
    )
    class_letter = forms.CharField(
        max_length=1,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'np: A'}),
        label='litera klasy:',
    )
    school = forms.CharField(
        max_length=128,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'np: ZSP Smolec'}),
        required=False, label='szkoła:',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        # self.helper.form_action = '' - zbadać do czego to jest
        self.helper.layout = Layout(
            Fieldset('Wprowadź dane dla tworzonej klasy:'),
            Row('semester', css_class='form-group col-md-2 mb-0'),

            Row(
                Column('class_number', css_class='form-group col-md-2 mb-0'),
                Column('class_letter', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row('school', css_class='form-group col-md-5 mb-0'),
            HTML('<br>'),
            ButtonHolder(
                Submit('submit', 'Utwórz klasę', css_class='btn btn-warning'),
                HTML('&nbsp'),
                Submit('submit', 'Powrót', css_class='btn btn-warning', onclick='history.back()'),
                css_class="d-flex justify-content-start"),
        )


class AddStudentsForm(forms.Form):
    students = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'np: \nKowalski Jan\nBrzęczyszczykiewicz Grzegorz\nBartolini Bartłomiej\n...',
        }),
        label='uczniowie:',
    )
    mask_lastnames = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        required=False, initial=True,
        label='maskuj nazwiska dla zgodności z RODO',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            HTML('''
        Wpisz listę uczniów w formacie Nazwisko Imię, w każdej linii jeden uczeń.<br>
        Można też przekopiować listę z Librusa:<br>
        - przejdź do Wiadomości/Napisz/Uczniowie<br>
        - rozwiń listę uczniów klasy, którą zamierzasz dodać<br>
        - za pomocą myszki skopiuj wszyskich uczniów, następnie wklej w oknie poniżej<br>
        (numery w dzienniku zostaną usunięte automatycznie)<br>
        <br>
        '''),

            Row('students', css_class='form-group col-md-11 mb-0'),
            Row('mask_lastnames'),
            HTML('<br>'),
            ButtonHolder(
                Submit('check', 'Sprawdź', css_class='btn btn-warning'),
                Submit('save', 'Zapisz', css_class='btn btn-warning'),
                css_class="d-flex justify-content-around"),
        )


class AddQuestionnaireForm(forms.Form):
    gradescale = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-select'}),
        choices=Gradescale.get_gradescale_choices(),
        label='wybierz skalę ocen:',
    )
    deadline = forms.DateTimeField(
        input_formats=['%Y-%m-%d %H:%M'],
        label='wskaż datę końcową na uzupełnienie ankiety przez uczniów:',
        required=False,
    )
    message_to_students = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'np: \n'
                           'Oceń zachowanie swoich koleżanek i kolegów. '
                           'Będzie to dla mnie ważna wskazówka przy wystawianiu ocen z zachowania.\n'
                           'Zapewniam, że ta ocena jest tylko dla mojej wiadomości.\n\n'
                           'Wasza wychowaczyni, X Y\n'
        }),
        label='wiadomość dla uczniów:',
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row('gradescale', css_class='form-group col-md-6 mb-0'),
            HTML('(nie będzie możliwości, aby zmienić skalę ocen po utworzeniu ankiety)<br>'),
            HTML('<br>'),
            Row('deadline', css_class='form-group col-md-6 mb-0'),
            HTML("""<script>$(function(){$("#id_deadline").datetimepicker({format: 'Y-m-d H:i',});});</script>"""),
            HTML('(jeżeli to pole zostanie puste, ankieta będzie otwarta do czasu jej "ręcznego" zamknięcia)<br>'),
            HTML('<br>'),
            Row('message_to_students', css_class='form-group col-md-6 mb-0'),
            HTML('(ta wiadomość pokaże się każdemu uczniowi przed właściwą częścią ankiety)<br>'),
            HTML('<br>'),
            ButtonHolder(
                Submit('save', 'Zapisz', css_class='btn btn-warning'),
                HTML('&nbsp'),
                Submit('return', 'Odrzuć', css_class='btn btn-warning'),
                css_class="d-flex justify-content-left "),
        )


class PersonalQuestionnaireForm(forms.Form):
    CHOICES = [('select1', 'select 1'),
               ('select2', 'select 2'),
               ('select3', 'select 5'),
               ]

    grade = forms.ChoiceField(
        widget=forms.RadioSelect(),
        choices=CHOICES,
        label='wystaw ocenę:',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            HTML('''
<div class="btn-group" role="group" aria-label="Basic radio toggle button group">
    <input type="radio" class="btn-check" name="grade" id="id_grade_0" value="select1">
    <label class="btn btn-outline-primary" for="id_grade_0">Radio 1</label>

    <input type="radio" class="btn-check" name="grade" id="id_grade_1" value="select2">
    <label class="btn btn-outline-primary" for="id_grade_1">Radio 2</label>

    <input type="radio" class="btn-check" name="grade" id="id_grade_2" value="select3">
    <label class="btn btn-outline-primary" for="id_grade_2">Radio 3</label>
</div>            
            '''),
            ButtonHolder(
                Submit('submit', 'Wyślij', css_class='btn btn-warning'),
                css_class="d-flex justify-content-left "),
        )


    # <div class="btn-group" role="group" aria-label="Basic radio toggle button group">
    #     <input type="radio" class="btn-check" name="btnradio" id="btnradio1" autocomplete="off">
    #     <label class="btn btn-outline-primary" for="btnradio1">Radio 1</label>
    #
    #     <input type="radio" class="btn-check" name="btnradio" id="btnradio2" autocomplete="off">
    #     <label class="btn btn-outline-waring" for="btnradio2">Radio 2</label>
    #
    #     <input type="radio" class="btn-check" name="btnradio" id="btnradio3" autocomplete="off">
    #     <label class="btn btn-outline-info" for="btnradio3">Radio 3</label>
    # </div>



# class AddQuestionnaireForm(forms.ModeldForm):
#     class Meta:
#         model = Questionnaire
#         fields = ['ext_description', 'deadline', 'is_stats_processed', 'gradescale']
#         labels = {
#             "ext_description": "opis",
#             "deadline": "Data końcowa na uzupełnienie ankiety"
#         }
