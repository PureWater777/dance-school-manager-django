from django import forms


class AddUserToCourseForm(forms.Form):
    student_email = forms.EmailField(max_length=60)
