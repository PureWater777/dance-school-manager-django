from django import forms

from dance_school_manager.settings import DAYS_OF_WEEK


class CreateCourseForm(forms.Form):
    name = forms.CharField(label='Course name', max_length=20)
    room = forms.IntegerField()
    description = forms.CharField(max_length=100)
    start_date = forms.DateField()
    days = forms.CharField(widget=forms.Select(choices=DAYS_OF_WEEK), max_length=70)
    time = forms.TimeField()
    end_date = forms.DateField()

    def __init__(self, *args, **kwargs):
        super(CreateCourseForm, self).__init__(*args, **kwargs)
        for i in range(20):
            self.fields[f'{i}_student'] = forms.EmailField(max_length=100, label=f'Student {i} email: ', required=False)