from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, HTML, ButtonHolder, Row, Column
from django import forms
from .views import Semester

class AddClassForm(forms.Form):
    semester = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control dropdown-toggle'}), choices=Semester.get_semester_choices(), label='wybierz semestr')
    class_number = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='cyfra klasy, np: 1    :')
    class_letter = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='litera klasy, np: A    :')
    school = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False, label='(opcjonalne) szkoła, np: ZSP w Smolcu:')
    students = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), label='uczniowie: ')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        # self.helper.form_action = '' - zbadać do czego to jest
        # self.helper.add_input(Submit('submit', 'Wyślij'))

        self.helper.layout = Layout(
            Fieldset('Wprowadź dane dla tworzonej klasy:'),
            Row('semester', css_class='form-group col-md-2 mb-0'),

            Row(
                Column('class_number', css_class='form-group col-md-2 mb-0'),
                Column('class_letter', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            'school',
            HTML('(najłatwiej wkleić listę uczniów przekopiowaną z Librusa, na razie nie przejmuj się RODO)'),
            'students',
            HTML('<br>'),
            ButtonHolder(
                Submit('submit', 'Utwórz klasę', css_class='btn btn-warning'),
                css_class="d-flex justify-content-end"),
        )
