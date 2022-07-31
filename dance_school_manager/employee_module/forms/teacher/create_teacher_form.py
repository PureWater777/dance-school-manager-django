from django import forms


class CreateTeacherForm(forms.Form):
    username = forms.CharField(label='Teacher username', max_length=20)
    email = forms.EmailField(max_length=60)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(CreateTeacherForm, self).__init__(*args, **kwargs)
        for i in range(20):
            self.fields[f'{i}_course'] = forms.CharField(label=f'Course {i} name', max_length=100, required=False)


class EditTeacherForm(forms.Form):
    username = forms.CharField(label='Teacher username', max_length=20)
    email = forms.EmailField(max_length=60)

    def __init__(self, *args, **kwargs):
        super(EditTeacherForm, self).__init__(*args, **kwargs)
        for i in range(20):
            self.fields[f'{i}_course'] = forms.CharField(label=f'Course {i} name', max_length=100, required=False)
