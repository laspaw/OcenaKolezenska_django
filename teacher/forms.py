from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, HTML, ButtonHolder, Row, Column
from django import forms
from .views import *
from .models import *


class AddClassForm(forms.Form):
    semester = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control dropdown-toggle'}),
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
    deadline = forms.DateTimeField(
        input_formats=['%Y.%m.%d %H:%M'],
        label='wskaż datę końcową na uzupełnienie ankiety przez uczniów:',
        required=False,
    )
    gradescale = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control dropdown-toggle'}),
        choices=Gradescale.get_gradescale_choices(),
        label='wybierz skalę ocen:',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row('gradescale', css_class='form-group col-md-4 mb-0'),
            HTML('(nie będzie możliwości, aby zmienić skalę ocen po utworzeniu ankiety)<br>'),
            HTML('<br>'),
            Row('deadline', css_class='form-group col-md-4 mb-0'),
            HTML("""<script>$(function(){$("#id_deadline").datetimepicker({format: 'Y.m.d H:i',});});</script>"""),
            HTML('(jeżeli to pole zostanie puste, ankieta będzie otwarta do czasu jej "ręcznego" zamknięcia)<br>'),
            HTML('<br>'),
            ButtonHolder(
                Submit('save', 'Zapisz', css_class='btn btn-warning'),
                HTML('&nbsp'),
                Submit('return', 'Odrzuć', css_class='btn btn-warning'),
                css_class="d-flex justify-content-left "),

        )

# class AddQuestionnaireForm(forms.ModeldForm):
#     class Meta:
#         model = Questionnaire
#         fields = ['ext_description', 'deadline', 'is_stats_processed', 'gradescale']
#         labels = {
#             "ext_description": "opis",
#             "deadline": "Data końcowa na uzupełnienie ankiety"
#         }
