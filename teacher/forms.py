from django import forms


class ContactForm(forms.Form):
    email = forms.EmailField()
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)
    send_to_me = forms.BooleanField(required=False)
