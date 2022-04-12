from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, HTML, ButtonHolder, Row, Column
from django import forms
from .views import Semester


class AddClassForm(forms.Form):
    semester = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control dropdown-toggle'}), choices=Semester.get_semester_choices(), label='wybierz semestr')
    class_number = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='cyfra klasy, np: 1    :')
    class_letter = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='litera klasy, np: A    :')
    school = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False, label='(opcjonalne) szkoła, np: ZSP Smolec')

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
    students = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), label='uczniowie: ')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            HTML('Wpisz ręcznie lub wklej z Librusa listę uczniów w formacie: Nazwisko Imię<br>'),
            HTML('W jednej linii jeden uczeń. Wszystkie znaki po imieniu zostaną zignorowane.<br>'),
            HTML('(na ten moment, nie przejmuj się RODO)'),

            Row('students', css_class='form-group col-md-5 mb-0'),
            HTML('<br>'),
            ButtonHolder(
                Submit('check', 'Sprawdź', css_class='btn btn-warning'),
                Submit('save', 'Zapisz', css_class='btn btn-warning'),
                css_class="d-flex justify-content-around"),

        )
