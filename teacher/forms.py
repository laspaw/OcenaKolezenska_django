from django import forms


class ContactForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    send_to_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

