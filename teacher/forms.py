from django import forms


class AddClassForm(forms.Form):
    class_number = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    class_letter = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    school = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))


#    students = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
