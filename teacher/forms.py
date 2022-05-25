from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, HTML, ButtonHolder, Row, Column, Div
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

from .views import *
from .models import *


class AddClassForm(forms.Form):
    class_number = forms.IntegerField(
        widget=forms.TextInput(attrs={'type': 'number', 'class': 'form-control', 'placeholder': 'np: 1'}),
        label='cyfra klasy:',
        validators=[MinValueValidator(0, message='Podaj liczbę większą od 0'),
                    MaxValueValidator(8, message='Podaj liczbę nie większą niż 8')],
    )
    class_letter = forms.CharField(
        max_length=1,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'np: A'}),
        label='litera klasy:',
        validators=[RegexValidator(regex='^[a-zA-Z]*$', message='Podaj literę'),
                    ]

    )
    school = forms.CharField(
        max_length=80,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'np: ZSP Smolec'}),
        required=False, label='szkoła:',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Div(
                Fieldset('Wprowadź dane dla tworzonej klasy:'),
                Div(
                    Column('class_number', css_class='form-group col-md-5'),
                    HTML('&nbsp'),
                    Column('class_letter', css_class='form-group col-md-5'),
                    css_class="d-flex flex-wrap justify-content-between py-3"),
                Row('school', css_class='form-group col-md-12'),
                ButtonHolder(
                    Submit('submit', 'Utwórz klasę', css_class='btn btn-warning'),
                    HTML('&nbsp'),
                    Submit('return', 'Powrót', css_class='btn btn-warning', onclick='history.back()'),
                    css_class="d-flex justify-content-around py-4"),
                css_class="form-check-inline"),
        )


class AddStudentsForm(forms.Form):
    students = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Nazwisko Imię\nnp: \nNiezgódka Adaś\nBrzęczyszczykiewicz Grzegorz\nBartolini Bartłomiej\n...',
        }),
        label='uczniowie:',
        max_length=2048,
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
Wpisz listę uczniów w formacie: <u>Nazwisko</u> Imię (każdy uczeń w osobnej linii).<br>
Można też przekopiować listę z Librusa:<br>
- w Librusie, przejdź do Wiadomości/Napisz/Uczniowie<br>
- rozwiń listę uczniów klasy, którą zamierzasz dodać<br>
- zaznacz, skopiuj i wklej wszystkich uczniów w oknie poniżej<br>
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
    class Meta:
        model = Questionnaire
        fields = ['deadline', 'message_to_students', 'gradescale']

    gradescale = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-select'}),
        choices=Gradescale.get_gradescale_choices(),
        # authors=forms.ModelMultipleChoiceField(queryset=Author.objects.all())
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
        }),
        label='wiadomość dla uczniów: (poniżej przykładowa wiadomość do ew. modyfikacji)',
        initial=''
                'Oceń zachowanie swoich koleżanek i kolegów.\n'
                'Będzie to dla mnie ważna wskazówka przy wystawianiu ocen z zachowania.\n'
                'Twoja ocena jest tylko dla mojej wiadomości.\n\n'
                'Wychowawca,\n',
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Div(
                Fieldset('Tworzenie ankiety:'),
                Div(
                    Row('gradescale', css_class='form-group col-md-12 mb-0'),
                    HTML('(nie będzie możliwości, aby zmienić skalę ocen po utworzeniu ankiety)<br>'),
                    css_class="my-4",
                ),
                Div(
                    Row('deadline', css_class='form-group col-md-12 mb-0'),
                    HTML("""<script>$(function(){$("#id_deadline").datetimepicker({format: 'Y-m-d H:i',});});</script>"""),
                    HTML('(jeżeli to pole zostanie puste, ankieta będzie otwarta do czasu jej "ręcznego" zamknięcia)<br>'),
                    css_class="my-4",
                ),
                Div(
                    Row('message_to_students', css_class='form-group col-md-12 mb-0'),
                    HTML('(ta wiadomość pokaże się każdemu uczniowi przy jego ankiecie)<br>'),
                    css_class="my-4",
                ),
                ButtonHolder(
                    Submit('save', 'Zapisz', css_class='btn btn-warning'),
                    HTML('&nbsp'),
                    Submit('return', 'Odrzuć', css_class='btn btn-warning'),
                    css_class="d-flex justify-content-around my-4"),
                css_class="form-check-inline text-start"),
        )


class PersonalQuestionnaireForm(forms.Form):
    styles = None
    class_obj = None

    def __init__(self, *args, **kwargs):
        self.grades = kwargs.pop('grades', None)
        self.class_obj = kwargs.pop('class_obj', None)
        self.answers = kwargs.pop('answers')
        self.grades_prefix = kwargs.pop('grades_prefix')

        super().__init__(*args, **kwargs)
        self.styles = self.render_styles(self.grades)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            HTML(self.render_button_radio_select()),
            HTML('<br>'),
            ButtonHolder(
                Submit('submit', 'Zapisz odpowiedzi', css_class='btn btn-warning'),
                css_class="d-flex justify-content-center "),
        )

    def render_button_radio_select(self):
        html_code = ''
        html_code += '<table>'

        for student in self.class_obj.student2class.all():
            html_code += '<tr>'
            html_code += f'<td style="padding-bottom: 1em;">{student.name}</td>'
            html_code += f'<td style="padding-bottom: 1em;">'
            for grade in self.grades:
                checked = 'checked=""' if self.answers.get(self.grades_prefix + str(student.id)) == grade.id else ''
                caption_or_svg_image = grade.caption if not grade.svg_icon else f'''
<svg width="48" height="48" fill="currentColor" class="bi bi-qr-code" viewBox="0 0 16 16">
<path d="{grade.svg_icon}"/>
</svg>                
            '''
                html_code += f'''
<input type="radio" class="btn-check" name="{self.grades_prefix}{student.id}" id="{student.id}_{grade.id}" value="{grade.id}" {checked}>
<label class="btn btn-outline-custom{grade.int_value}" for="{student.id}_{grade.id}">{caption_or_svg_image}</label>
                    '''
            html_code += '</td>'
            html_code += '</tr>'

        html_code += '</table>'
        return html_code

    @staticmethod
    def render_styles(grades):
        styles = ''
        for grade in grades:
            bg_color = grade.bg_color
            styles += f'''
.btn-outline-custom{grade.int_value}
{{color:grey;background-color:{bg_color}20;border-color:{bg_color}}}
.btn-outline-custom{grade.int_value}:hover,.btn-check:active+.btn-outline-custom{grade.int_value},.btn-check:checked+.btn-outline-custom{grade.int_value},.btn-outline-custom{grade.int_value}.active,.btn-outline-custom{grade.int_value}.dropdown-toggle.show,.btn-outline-custom{grade.int_value}:active
{{color:white;background-color:{bg_color};border-color:{bg_color}}}
.btn-check:active+.btn-outline-custom{grade.int_value}:focus,.btn-check:checked+.btn-outline-custom{grade.int_value}:focus,.btn-outline-custom{grade.int_value}.active:focus,.btn-outline-custom{grade.int_value}.dropdown-toggle.show:focus,.btn-outline-custom{grade.int_value}:active:focus,.btn-check:focus+.btn-outline-custom{grade.int_value},.btn-outline-custom{grade.int_value}:focus
{{box-shadow:0 0 0 .25rem rgba(165, 150, 147,.3)}}
            '''
        return styles
