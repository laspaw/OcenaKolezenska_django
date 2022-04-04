from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, HTML, ButtonHolder
from django import forms


class AddClassForm(forms.Form):
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
            Fieldset('Wprowadź dane dla tworzonej klasy:',
                     'class_number',
                     'class_letter',
                     'school',
                     'description',
                     HTML('(najłatwiej wkleić listę uczniów przekopiowaną z Librusa, na razie nie przejmuj się RODO)'),
                     'students',
                     ),
            ButtonHolder(
                Submit('submit', 'Wyślij', css_class='btn btn-warning'),
                css_class="d-flex justify-content-end")
        )
