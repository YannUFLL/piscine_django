from django import forms

class MyForm(forms.Form):
    text = forms.CharField(label="Your text", max_length=100)
