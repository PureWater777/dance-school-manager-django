from django import forms


class SimpleExceptionForm(forms.Form):
    name = forms.CharField(max_length=20)
    date = forms.DateField()
    description = forms.CharField(max_length=100)


class GeneralExceptionForm(forms.Form):
    name = forms.CharField(max_length=20)
    date = forms.DateField()
    description = forms.CharField(max_length=100)

